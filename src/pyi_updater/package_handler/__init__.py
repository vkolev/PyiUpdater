from __future__ import print_function
import json
import logging
import multiprocessing
import os
import shutil

try:
    import bsdiff4
except ImportError:
    bsdiff4 = None

from pyi_updater.exceptions import PackageHandlerError
from pyi_updater.package_handler.package import Package, Patch
from pyi_updater.utils import (EasyAccessDict,
                               get_package_hashes as gph,
                               lazy_import,
                               migrate,
                               remove_dot_files
                               )

log = logging.getLogger(__name__)

jms_utils = None


class PackageHandler(object):
    """Handles finding, sorting, getting meta-data, moving packages.

    Kwargs:
        app (instance): Config object to get config values from
    """

    data_dir = None

    def __init__(self, app=None):
        global jms_utils
        jms_utils = lazy_import('jms_utils')
        self.config_loaded = False
        self.init = False
        if app:
            self.init_app(app)

    def init_app(self, obj):
        """Sets up client with config values from obj

        Args:
            obj (instance): config object

        """
        self.patches = obj.get(u'UPDATE_PATCHES', True)
        if self.patches:
            log.debug(u'Looks like were ready to make some patches')
            self.patch_support = True
        else:
            log.debug(u'Looks like its not patch time.')
            self.patch_support = False
        self.data_dir = obj.get(u'DEV_DATA_DIR')
        if self.data_dir is not None:
            self.data_dir = os.path.join(self.data_dir, u'pyi-data')
            self.files_dir = os.path.join(self.data_dir, u'files')
            self.deploy_dir = os.path.join(self.data_dir, u'deploy')
            self.new_dir = os.path.join(self.data_dir, u'new')
            self.config_dir = os.path.join(os.path.dirname(self.data_dir),
                                           u'.pyiupdater')
            self.config_file = os.path.join(self.config_dir, 'data.json')
            self.config = None
        else:
            log.debug('DEV_DATA_DIR is None. Setup Failed')

        self.json_data = None
        if self.data_dir is not None:
            self.init = True
            if os.path.exists(self.config_file) is False and \
                    os.path.exists(self.files_dir) is True:
                migrate(self.data_dir)

        self.setup()

    def setup(self):
        """Creates all needed working directories & loads json files.

        Proxy method for :meth:`_setup_work_dirs` & :meth:`_load_version_file`
        """
        if self.data_dir is not None:
            self._setup()

    def _setup(self):
        self._setup_work_dirs()
        if self.config_loaded is False:
            self.json_data = self._load_version_file()
            self.config = self._load_config()
            self.config_loaded = True

    def process_packages(self):
        """Gets a list of updates to process.  Adds the name of an
        update to the version file if not already present.  Processes
        all packages.  Updates the version file meta-data. Then writes
        version file back to disk.

        Proxy method for :meth:`_get_package_list`,
        :meth:`_make_patches`, :meth:`_add_patches_to_packages`,
        :meth:`_update_version_file`,
        :meth:`_write_json_to_file` & :meth:`_move_packages`.
        """
        if self.init is False:
            raise PackageHandlerError('Must init first.', expected=True)
        package_manifest, patch_manifest = self._get_package_list()
        patches = self._make_patches(patch_manifest)
        self._cleanup(patch_manifest)
        package_manifest = self._add_patches_to_packages(package_manifest,
                                                         patches)
        self.json_data = self._update_version_file(self.json_data,
                                                   package_manifest)
        self._write_json_to_file(self.json_data)
        self._write_config_to_file(self.config)
        self._move_packages(package_manifest)

    def _setup_work_dirs(self):
        # Sets up work dirs on dev machine.  Creates the following folder
        #    - Data dir
        # Then inside the data folder it creates 3 more folders
        #    - New - for new updates that need to be signed
        #    - Deploy - All files ready to upload are placed here.
        #    - Files - All updates are placed here for future reference
        #
        # This is non destructive
        log.debug(u'Setting up work dirs...')
        dirs = [self.data_dir, self.new_dir,
                self.deploy_dir, self.files_dir,
                self.config_dir]
        for d in dirs:
            if not os.path.exists(d):
                os.mkdir(d)

    def _load_version_file(self):
        # If version file is found its loaded to memory
        # If no version file is found then one is created.
        json_data = None
        log.debug(u'Looking for version file...')
        version_file = os.path.join(self.data_dir, u'version.json')
        if os.path.exists(version_file):
            with open(version_file) as f:
                log.debug(u'Loading version file...')
                try:
                    json_data = json.loads(f.read())
                    log.debug(u'Found version file, now reading')
                except Exception as err:
                    log.error(str(err))

            if json_data is not None:
                updates = json_data.get(u'updates')
                log.debug(u'Checking for valid data in version file...')
                if updates is None:
                    log.debug(u'Invalid data in version file...')
                    json_data[u'updates'] = {}
                    log.debug(u'Updated version file format')

        if json_data is None:
            log.error(u'Version file not found')
            json_data = {'updates': {}}
            log.debug(u'Created new version file')
        log.debug(u'Loaded version file')
        return json_data

    def _load_config(self):
        config = None
        log.debug(u'Looking for config file...')
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, u'r') as f:
                    config = json.loads(f.read())
            except Exception as err:
                log.debug(str(err))

        if config is None:
            config = {
                u'patches': {}
                }
        return config

    def _get_package_list(self, ignore_errors=True):
        # Adds compatible packages to internal package manifest
        # for futher processing
        # Process all packages in new folder and gets
        # url, hash and some outer info.
        log.debug(u'Getting package list')
        # Clears manifest if sign updates runs more the once without
        # app being restarted
        package_manifest = list()
        patch_manifest = list()
        bad_packages = list()
        with jms_utils.paths.ChDir(self.new_dir):
            # Getting a list of all files in the new dir
            packages = os.listdir(os.getcwd())
            for p in packages:
                # On package initialization we do the following
                # 1. Check for a supported archive
                # 2. get required info: version, platform, hash
                # If any check fails package.info['status'] will be False
                # You can query package.info['reason'] for the reason
                package = Package(p)
                if package.info['status'] is False:
                    # Package failed at something
                    # package.info['reason'] will tell why
                    bad_packages.append(package)
                    continue

                self.json_data = self._update_file_list(self.json_data,
                                                        package)

                package_manifest.append(package)
                self.config = self._add_package_to_config(package,
                                                          self.config)

                if self.patch_support:
                    # Will check if source file for patch exists
                    # if so will return the path and number of patch
                    # to create. If missing source file None returned
                    path = self._check_make_patch(self.json_data,
                                                  package.name,
                                                  package.platform,
                                                  )
                    if path is not None:
                        log.debug(u'Found source file to create patch')
                        patch_name = package.name + u'-' + package.platform
                        src_path = path[0]
                        patch_number = path[1]
                        patch_info = dict(src=src_path,
                                          dst=os.path.abspath(p),
                                          patch_name=os.path.join(self.new_dir,
                                                                  patch_name),
                                          patch_num=patch_number,
                                          package=package.filename)
                        # ready for patching
                        patch_manifest.append(patch_info)
                    else:
                        log.debug(u'No patch source file')

        # ToDo: Expose this
        if ignore_errors is False:
            print(u'Bad package & reason for being naughty:')
            for b in bad_packages:
                print(b.name, b.info['reason'])

        return package_manifest, patch_manifest

    def _add_package_to_config(self, p, data):
        if 'package' not in data.keys():
            data['package'] = {}
            log.debug('Initilizing config for packages')
        # First package with current name so add platform and version
        if p.name not in data['package'].keys():
            data['package'][p.name] = {p.platform: p.version}
            log.debug('Adding new package to config')
        else:
            # Adding platform and version
            if p.platform not in data['package'][p.name].keys():
                data['package'][p.name][p.platform] = p.version
                log.debug('Adding new arch to package-config')
            else:
                # Getting current version for platform
                value = data['package'][p.name][p.platform]
                # Updating version if applicable
                if p.version > value:
                    log.debug('Adding new version to package-config')
                    data['package'][p.name][p.platform] = p.version
        return data

    def _cleanup(self, patch_manifest):
        for p in patch_manifest:
            if os.path.exists(p[u'src']):
                os.remove(p[u'src'])

    def _make_patches(self, patch_manifest):
        pool_output = list()
        log.debug(u'Staring patch creation')
        cpu_count = multiprocessing.cpu_count() * 2
        pool = multiprocessing.Pool(processes=cpu_count)
        pool_output = pool.map(_make_patch, patch_manifest)
        return pool_output

    def _add_patches_to_packages(self, package_manifest, patches):
        # ToDo: Increase the efficiency of this double for
        #       loop. Not sure if it can be done though
        log.debug(u'Adding patches to package list')
        if patches is not None:
            log.debug('We got patches...')
            for p in patches:
                if p.ready is False:
                    continue
                for pm in package_manifest:
                    if p.dst_filename == pm.filename:
                        pm.patch_info[u'patch_name'] = \
                            os.path.basename(p.patch_name)
                        if not os.path.exists(p.patch_name):
                            p_name = ''
                        else:
                            p_name = gph(p.patch_name)
                        pm.patch_info[u'patch_hash'] = p_name
                        break
                    else:
                        log.debug('No patch match found')
        return package_manifest

    def _update_version_file(self, json_data, package_manifest):
        # Updates version file with package meta-data
        log.debug(u'Starting version file update')
        easy_dict = EasyAccessDict(json_data)
        for p in package_manifest:
            patch_name = p.patch_info.get(u'patch_name')
            patch_hash = p.patch_info.get(u'patch_hash')

            # Converting info to version file format
            info = {u'file_hash': p.file_hash,
                    u'filename': p.filename}
            if patch_name and patch_hash:
                info[u'patch_name'] = patch_name
                info[u'patch_hash'] = patch_hash

            version_key = '{}*{}*{}'.format(u'updates', p.name, p.version)
            version = easy_dict.get(version_key)
            log.debug(u'Package info {}'.format(version))

            if version is None:
                log.debug(u'Adding new version to file')

                # First version this package name
                json_data[u'updates'][p.name][p.version] = {}
                platform_key = '{}*{}*{}*{}'.format(u'updates', p.name,
                                                    p.version, u'platform')

                platform = easy_dict.get(platform_key)
                if platform is None:
                    name_ = json_data[u'updates'][p.name]
                    name_[p.version][p.platform] = info

            else:
                # package already present, adding another version to it
                log.debug(u'Appending info data to version file')
                json_data[u'updates'][p.name][p.version][p.platform] = info

            # Will add each individual platform version update
            # to latest.  Now can update platforms independently
            json_data[u'latest'][p.name][p.platform] = p.version
        return json_data

    def _write_json_to_file(self, json_data):
        # Writes json data to disk
        log.debug(u'Writing version data to file')
        with open(os.path.join(self.data_dir, u'version.json'), u'w') as f:
            f.write(json.dumps(json_data, sort_keys=True, indent=4))

    def _write_config_to_file(self, json_data):
        log.debug(u'Writing config data to file')
        with open(self.config_file, u'w') as f:
            f.write(json.dumps(json_data, sort_keys=True, indent=2))

    def _move_packages(self, package_manifest):
        log.debug(u'Moving packages to deploy folder')
        for p in package_manifest:
            patch = p.patch_info.get(u'patch_name')
            with jms_utils.paths.ChDir(self.new_dir):
                if patch:
                    if os.path.exists(os.path.join(self.deploy_dir, patch)):
                        os.remove(os.path.join(self.deploy_dir, patch))
                    log.debug(u'Moving {} to {}'.format(patch,
                              self.deploy_dir))
                    if os.path.exists(patch):
                        shutil.move(patch, self.deploy_dir)

                shutil.copy(p.filename, self.deploy_dir)
                log.debug(u'Copying {} to {}'.format(p.filename,
                          self.deploy_dir))

                if os.path.exists(os.path.join(self.files_dir, p.filename)):
                    os.remove(os.path.join(self.files_dir, p.filename))
                shutil.move(p.filename, self.files_dir)
                log.debug(u'Moving {} to {}'.format(p.filename,
                          self.files_dir))

    def _update_file_list(self, json_data, package_info):
        files = json_data[u'updates']
        latest = json_data.get(u'latest')
        if latest is None:
            json_data[u'latest'] = {}
        file_name = files.get(package_info.name)
        if file_name is None:
            log.debug(u'Adding {} to file list'.format(package_info.name))
            json_data[u'updates'][package_info.name] = {}

        latest_package = json_data[u'latest'].get(package_info.name)
        if latest_package is None:
            json_data[u'latest'][package_info.name] = {}
        return json_data

    def _check_make_patch(self, json_data, name, platform):
        # Check to see if previous version is available to
        # make patch updates
        # Also calculates patch number
        log.debug('Checking if patch creation is possible')
        if bsdiff4 is None:
            return None
        src_file_path = None
        if os.path.exists(self.files_dir):
            with jms_utils.paths.ChDir(self.files_dir):
                files = os.listdir(os.getcwd())

            files = remove_dot_files(files)
            # No src files to patch from. Exit quickly
            if len(files) == 0:
                return None
            # If latest not available in version file. Exit
            try:
                latest = json_data[u'latest'][name][platform]
            except KeyError:
                return None
            try:
                l_plat = json_data[u'updates'][name][latest][platform]
                filename = l_plat[u'filename']
            except:
                return None
            src_file_path = os.path.join(self.files_dir, filename)

            try:
                patch_num = self.config[u'patches'][name]
                self.config[u'patches'][name] += 1
            except KeyError:
                # If no patch number we will start at 100
                try:
                    patch_num = self.config[u'boot_strap']
                except KeyError:
                    patch_num = 100
                if u'patches' not in self.config.keys():
                    self.config[u'patches'] = {}
                if name not in self.config[u'patches'].keys():
                    self.config[u'patches'][name] = patch_num + 1
            num = patch_num + 1
            log.debug('Patch Number: {}'.format(num))
            return src_file_path, num
        return None


def _make_patch(patch_info):
    # Does with the name implies. Used with multiprocessing
    patch = Patch(patch_info)
    patch_name = patch_info[u'patch_name']
    dst_path = patch_info[u'dst']
    patch_number = patch_info[u'patch_num']
    src_path = patch_info[u'src']
    patch_name += u'-' + str(patch_number)
    # Updating with full name - number included
    patch.patch_name = patch_name
    if not os.path.exists(src_path):
        log.debug('Src file does not exist to create patch')

    else:
        print(u"Making patch... {}".format(os.path.basename(patch_name)))
        log.debug(u'Patch source path:{}'.format(src_path))
        log.debug(u'Patch destination path: {}'.format(dst_path))
        if patch.ready is True:
            log.debug(u'Creating patch')
            bsdiff4.file_diff(src_path, patch.dst_path, patch.patch_name)
            log.debug(u'Done creating patch')
        else:
            log.debug('Missing patch attr')
    return patch
