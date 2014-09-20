from __future__ import print_function
import json
import logging
import multiprocessing
import os
import shutil
import sys

try:
    import bsdiff4
except ImportError:
    bsdiff4 = None
from jms_utils import ChDir
from six.moves import input

from pyi_updater.package_handler.package import Package
from pyi_updater.utils import (FROZEN,
                               get_package_hashes,
                               remove_dot_files,
                               version_string_to_tuple,
                               version_tuple_to_string,
                               )

log = logging.getLogger(__name__)


class PackageHandler(object):
    """Handles finding, sorting, getting meta-data, moving packages.

    Kwargs:
        app (instance): Config object to get config values from
    """

    data_dir = None

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, obj):
        """Sets up client with config values from obj

        Args:
            obj (instance): config object

        """
        self.app_dir = obj.config.get(u'APP_DIR')

        self.patches = obj.config.get(u'UPDATE_PATCHES', True)
        if self.patches:
            log.debug(u'Looks like were ready to make some patches')
            self.patch_support = True
        else:
            log.debug(u'Looks like its not patch time.')
            self.patch_support = False
        self.data_dir = obj.config.get(u'DEV_DATA_DIR')
        if self.data_dir is not None:
            self.data_dir = os.path.join(self.data_dir, u'pyi-data')
            self.files_dir = os.path.join(self.data_dir, u'files')
            self.deploy_dir = os.path.join(self.data_dir, u'deploy')
            self.new_dir = os.path.join(self.data_dir, u'new')
        else:
            log.warning('DEV_DATA_DIR is None. Setup Failed')

        self.update_url = obj.config.get(u'UPDATE_URL')

        self.json_data = None
        self.package_manifest = []

    def setup(self):
        """Creates all needed working directories & loads version file.

        Proxy method for :meth:`_setup_work_dirs` & :meth:`_load_version_file`
        """
        self._setup_work_dirs()
        self._load_version_file()

    def update_package_list(self):
        """Gets a list of updates to process.  Adds the name of an
        update to the version file if not already present.  Processes
        all packages.  Updates the version file meta-data. Then writes
        version file back to disk.

        Proxy method for :meth:`_get_package_list`,
        :meth:`_setup_file_dirs`, :meth:`_update_version_file` &
        :meth:`_write_json_to_file`.
        """
        self._get_package_list()
        self._setup_file_dirs()
        self._update_version_file()
        self._write_json_to_file()

    def deploy(self):
        """Moves updates/patches/version file to deploy folder

        Proxy method form :meth:`_move_packages`
        """
        self._move_packages()

    def _setup_work_dirs(self):
        # Sets up work dirs on dev machine.  Creates the following folder
        #    - Data dir
        # Then inside the data folder it creates 3 more folders
        #    - New - for new updates that need to be signed
        #    - Deploy - All files ready to upload are placed here.
        #    - Files - All updates are placed here for future reference
        #
        # This is non destructive
        log.info(u'Setting up work dirs...')
        dirs = [self.data_dir, self.new_dir, self.deploy_dir, self.files_dir]
        for d in dirs:
            if not os.path.exists(d):
                os.mkdir(d)

    def _load_version_file(self):
        # If version file is found its loaded to memory
        # If no version file is found then one is created.
        log.debug(u'Looking for version file...')
        version_file = os.path.join(self.data_dir, u'version.json')
        if os.path.exists(version_file):
            with open(version_file) as f:
                log.info(u'Loading version file...')
                try:
                    self.json_data = json.loads(f.read())
                    log.debug(u'Found version file, now reading')
                except Exception as err:
                    log.error(str(err))
                    self.json_data = None

            if self.json_data is not None:
                updates = self.json_data.get(u'updates', None)
                log.debug(u'Checking for valid data in version file...')
                if updates is None:
                    log.debug(u'Invalid data in version file...')
                    self.json_data[u'updates'] = {}
                    log.debug(u'Updated version file format')
            else:
                self.json_data = {'updates': {}}
                log.debug(u'Created new version file')
        else:
            log.error(u'Version file not found')
            self.json_data = {'updates': {}}
            log.debug(u'Created new version file')
        log.info(u'Loaded version file')

    def _get_package_list(self, ignore_errors=True):
        # Adds compatible packages to internal package manifest
        # for futher processing
        # Process all packages in new folder and gets
        # url, hash and some outer info.
        log.info(u'Getting package list')
        # Clears manifest if sign updates runs more the once without
        # app being restarted
        if len(self.package_manifest) != 0:
            self.package_manifest = []

        with ChDir(self.new_dir):
            # Getting a list of all files in the new dir
            bad_packages = []
            patch_manifest = []
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

                self._update_file_list(package)

                self.package_manifest.append(package)

                if self.patch_support:
                    # Will check if source file for patch exists
                    # if so will return the path and number of patch
                    # to create. If missing source file None returned
                    path = self._check_make_patch(package.name,
                                                  package.version,
                                                  package.platform)
                    if path is not None:
                        platform_patch_name = package.name + u'-' + \
                            package.platform
                        src_path = path[0]
                        patch_number = path[1]
                        patch_info = dict(src=src_path, dst=p,
                                          patch_name=platform_patch_name,
                                          patch_num=patch_number,
                                          package=package.filename)
                        # ready for patching
                        patch_manifest.append(patch_info)

            # When the framework is frozen with pyinstaller I got
            # weird issues with multiprocessing. If you can fix
            # the issue a PR is greatly appreciated
            if FROZEN and sys.platform == u'win32':
                pool_output = []
                for p in patch_manifest:
                    patch_output = _make_patch(p)
                    pool_output.append(patch_output)
            else:
                cpu_count = multiprocessing.cpu_count() * 2
                pool = multiprocessing.Pool(processes=cpu_count)
                pool_output = pool.map(_make_patch, patch_manifest)

            # ToDo: Increase the efficiency of this double for
            #       loop. Not sure if it can be but it just
            #       looks like it wastes time.
            for i in pool_output:
                for s in self.package_manifest:
                    if i[0] == s.filename:
                        s.patch_info[u'patch_name'] = i[1]
                        s.patch_info[u'patch_hash'] = get_package_hashes(i[1])
                        break

        # ToDo: Expose this
        if ignore_errors is False:
            print(u'Bad package & reason for being naughty:')
            for b in bad_packages:
                print(b.name, b.info['reason'])

    def _setup_file_dirs(self):
        log.info(u'Setting up directories for file updates')
        for p in self.package_manifest:
            package_dir = os.path.join(self.files_dir, p.name)
            package_version_path = os.path.join(package_dir, p.version)
            p.version_path = package_version_path
            # Creating a dir for specific package
            if not os.path.exists(package_dir):
                os.mkdir(package_dir)
            # Creating a dir for specific version of above package
            if not os.path.exists(package_version_path):
                os.mkdir(package_version_path)

    def _update_version_file(self):
        # Updates version file with package meta-data
        log.info(u'Starting version file update')
        for p in self.package_manifest:
            patch_name = p.patch_info.get(u'patch_name', None)
            patch_hash = p.patch_info.get(u'patch_hash', None)

            # Converting info to version file format
            info = {u'file_hash': p.file_hash,
                    u'filename': p.filename}
            if patch_name and patch_hash:
                info[u'patch_name'] = patch_name
                info[u'patch_hash'] = patch_hash

            log.debug(u'json version {}'.format(self.json_data[u'updates']
                      [p.name].get(p.version, None)))

            if self.json_data[u'updates'][p.name].get(p.version,
                                                      None) is None:
                log.debug(u'Adding new version to file')

                # First version this package name
                self.json_data[u'updates'][p.name][p.version] = {}
                temp_platform = self.json_data[u'updates'][p.name][p.version]
                temp_platform = temp_platform.get(u'platform', None)
                if temp_platform is None:
                    name_ = self.json_data[u'updates'][p.name]
                    name_[p.version][p.platform] = info

            else:
                # package already present, adding another version to it
                log.debug(u'Appending info data to version file')
                self.json_data[u'updates'][p.name][p.version][p.platform] = \
                    info

            # Will add each individual platform version update
            # to latest.  Now can update platforms independently
            self.json_data[u'latest'][p.name][p.platform] = p.version

    def _write_json_to_file(self):
        # Writes json data to disk
        log.info(u'Writing version data to file')
        with open(os.path.join(self.data_dir, u'version.json'), u'w') as f:
            f.write(json.dumps(self.json_data, sort_keys=True, indent=4))

    # ToDo: Explain whats going on below &/or clean up
    def _move_packages(self):
        # Moves all packages to their destination folder.
        # Destination is figured by lib name and version number.
        # Since we are copying files to the deploy folder then
        # moving the updates to the files folder, we can safely
        # delete files in deploy folder after uploading.
        log.info(u'Moving packages to deploy folder')
        for p in self.package_manifest:
            patch = p.patch_info.get(u'patch_name', None)
            version_path = p.version_path
            with ChDir(self.new_dir):
                if patch:
                    shutil.copy(patch, self.deploy_dir)
                    log.debug(u'Copying {} to {}'.format(patch,
                              self.deploy_dir))
                    shutil.move(patch, version_path)
                    log.debug(u'Moving {} to {}'.format(patch, version_path))

                shutil.copy(p.filename, self.deploy_dir)
                log.debug(u'Copying {} to {}'.format(p.filename,
                          self.deploy_dir))

                if os.path.exists(os.path.join(version_path, p.filename)):
                    msg = (u'Version {} of {} already exists.  Overwrite?\n'
                           '[N/y]-->'.format(p['version'], p['name']))

                    answer = input(msg)
                    if answer.lower() in [u'yes', u'ye', u'y']:
                        shutil.rmtree(version_path, ignore_errors=True)
                        os.mkdir(version_path)
                        shutil.move(p.filename, version_path)
                    else:
                        continue
                else:
                    shutil.move(p.filename, version_path)
                    log.debug(u'Moving {} to {}'.format(p.filename,
                              version_path))

        # I freaking love this chdir context manager!!!
        with ChDir(self.data_dir):
            shutil.copy(u'version.json', self.deploy_dir)

    def _update_file_list(self, package_info):
        files = self.json_data[u'updates']
        latest = self.json_data.get(u'latest', None)
        if latest is None:
            self.json_data[u'latest'] = {}
        file_name = files.get(package_info.name, None)
        if file_name is None:
            log.info(u'Adding {} to file list'.format(package_info.name))
            self.json_data[u'updates'][package_info.name] = {}

        latest_package = self.json_data[u'latest'].get(package_info.name, None)
        if latest_package is None:
            self.json_data[u'latest'][package_info.name] = {}

    def _check_make_patch(self, name, version_str, platform):
        # Check to see if previous version is available to
        # make patch updates
        # Also calculates patch number
        version = version_string_to_tuple(version_str)
        if bsdiff4 is None:
            return None
        src_file_path = None
        data_dir = os.path.join(self.files_dir, name)
        if os.path.exists(data_dir):
            with ChDir(data_dir):
                # getting a list of all version folders
                # for current app
                version_dirs = os.listdir(os.getcwd())
                version_dirs = remove_dot_files(version_dirs)

                # Changing version strings into tuples
                fixed_version_dirs = []
                for v in version_dirs:
                    fixed_version_dirs.append(version_string_to_tuple(v))

                # Can't make a patch if no source file to work with
                if len(fixed_version_dirs) < 1:
                    return None

                highest_version = sorted(fixed_version_dirs)[-1]
                highest_version_str = version_tuple_to_string(highest_version)

                if highest_version > version:
                    return None

            # Chainging into directory to get absolute path of
            # source file for patch creation later
            target_dir = os.path.join(data_dir, highest_version_str)
            with ChDir(target_dir):
                files = remove_dot_files(os.listdir(os.getcwd()))
                # If somehow the source file got deleted
                # just return
                if len(files) == 0:
                    return None
                # Getting the correct source matches
                # destination platform
                for f in files:
                    if highest_version_str in f and platform in f:
                        src_file_path = os.path.abspath(f)
                        break
            # if our list gets exhausted before finding
            # source file then just return None
            if src_file_path is None:
                return None
            return src_file_path, len(fixed_version_dirs) + 1


def _make_patch(patch_info):
    # Does with the name implies. Used with multiprocessing
    patch_name = patch_info[u'patch_name']
    patch_number = patch_info[u'patch_num']
    src_path = patch_info[u'src']
    dst_path = patch_info[u'dst']
    print(u"Patch name: {}".format(patch_name))
    print(u'Patch number: {}'.format(patch_number))
    print(u'Src: {}'.format(src_path))
    print(u'Dst: {}'.format(dst_path))

    patch_name += u'-' + str(patch_number)
    log.info(u'Creating patch')
    bsdiff4.file_diff(src_path, dst_path, patch_name)
    log.info(u'Done creating patch')
    return dst_path, patch_name
