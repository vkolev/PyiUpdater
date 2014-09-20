import json
import logging
import os
import shutil
import sys
import tarfile
from zipfile import ZipFile

from appdirs import user_cache_dir
from jms_utils import ChDir, get_system
import requests

from pyi_updater.archiver import make_archive
from pyi_updater.config import Config
from pyi_updater.downloader import FileDownloader
from pyi_updater.exceptions import ClientError, UtilsError
from pyi_updater.patcher import Patcher
from pyi_updater.utils import (DotAccessDict, FROZEN, rsa_verify, get_version_number,
                               version_string_to_tuple)

log = logging.getLogger(__name__)

platform_ = get_system()


class Client(object):
    """Used on client side to update files

    Kwargs:

        obj (instance): config object
    """

    def __init__(self, obj=None, test=False):
        if obj:
            self.init_app(obj, test)

    def init_app(self, obj, test=False):
        """Sets up client with config values from obj

        Args:
            obj (instance): config object

        """
        # ToDo: Remove once code is v1.0
        #       Updated how client is initialized.  Can still be
        #       used the old way but the new way is way more efficient
        #       Just pass in the config object and the client takes care
        #       of the rest.  No need to initialize NotSoTuf object first!
        if hasattr(obj, 'config'):
            config = obj.config.copy()
        else:
            config = Config()
            config.from_object(obj)

        # Grabbing config information
        self.update_url = self._fix_update_url(config.get(u'UPDATE_URL'))
        self.app_name = config.get(u'APP_NAME')
        self.company_name = config.get(u'COMPANY_NAME', u'Digital Sapphire')
        if test:
            self.data_dir = 'cache'
        else:
            self.data_dir = user_cache_dir(self.app_name, self.company_name)
        self.update_folder = os.path.join(self.data_dir, u'update')
        self.public_key = config.get(u'PUBLIC_KEY', None)
        self.debug = config.get(u'DEBUG', False)
        self.verify = config.get(u'VERIFY_SERVER_CERT', True)
        self.version_file = u'version.json'
        self.version_url = self.update_url + self.version_file

        self.name = None
        self.version = None
        self.json_data = None
        self.verified = False
        self.ready_to_update = False
        self.updates_key = u'updates'
        self.current_app_dir = os.path.dirname(sys.argv[0])

        self._setup()
        self.refresh()

    def refresh(self):
        """Will download and verify your updates version file.

        Proxy method from :meth:`_get_update_manifest`.
        """
        try:
            self._get_update_manifest()
        except Exception as err:
            log.debug(str(err), exc_info=True)

    def update_check(self, name, version):
        """
        Will try to patch binary if all check pass.  IE hash verified
        signature verified.  If any check doesn't pass then falls back to
        full update

        Args:
            name (str): Name of file to update

            version (str): Current version number of file to update

        Returns:
            (bool) Meanings::

                True - Update Successful

                False - Update Failed
        """
        self.name = name
        self.version = version

        if FROZEN and self.name == self.app_name:
            # We only add .exe to app executable.  Not libs or dll
            self._archive_installed_binary()
        # Removes old versions, of update being checked, from
        # updates folder.  Since we only start patching from
        # the current binary this shouldn't be a problem.
        self._remove_old_updates()

        # Checking if version file is verified before
        # processing data contained in the version file.
        # This was done by self._get_update_manifest()
        if not self.verified:
            return False
        log.info(u'Checking for {} updates...'.format(name))

        # If None is returned self._get_highest_version could
        # not find the supplied name in the version
        latest = self._get_highest_version(name)
        if latest is None:
            return False
        if version_string_to_tuple(latest) <= \
                version_string_to_tuple(version):
            log.debug(u'{} already updated to the latest version'.format(name))
            log.info(u'Already up-to-date')
            return False
        # Hey, finally made it to the bottom!
        # Looks like its time to do some updating
        log.info(u'Update available')
        self.ready_to_update = True
        return True

    def download(self):
        """Will securely download the package update that was called
        with check update.

        Proxy method for :meth:`_patch_update` & :meth:`_full_update`.
        """
        if self.ready_to_update is False:
            return False
        patch_success = self._patch_update(self.name, self.version)
        if patch_success:
            log.info(u'Download successful')
        else:
            update_success = self._full_update(self.name)
            if update_success:
                log.info(u'Download successful')
            else:
                return False
        return True

    def install_restart(self):
        """ Will install (unzip) the update, overwrite the current app,
        then restart the app using the updated binary.

        On windows Proxy method for :meth:`_extract_update` &
        :meth:`_win_overwrite_app_restart`

        On unix Proxy method for :meth:`_extract_update`,
        :meth:`_overwrite_app` & :meth:`_restart`
        """
        try:
            self._extract_update()

            if get_system() == u'win':
                self._win_overwrite_app_restart()
            else:
                self._overwrite_app()
                self._restart()
        except ClientError as err:
            log.error(str(err), exc_info=True)

    def install(self):
        """Will extract archived update and leave in update folder.
        If updating a lib you can take over from there. If updating
        an app this call should be followed by :meth:`restart` to
        complete update.

        Proxy method for :meth:`_extract_update`.
        """
        if get_system() == u'win':
            log.warning('Only supported on Unix like systems')
            return
        try:
            self._extract_update()
        except ClientError as err:
            log.error(str(err), exc_info=True)

    def restart(self):
        """Will overwrite old binary with updated binary and
        restart using the updated binary.

        Proxy method for :meth:`_overwrite_app` & :meth:`_restart`.
        """
        if get_system() == u'win':
            log.warning(u'Only supported on Unix like systems')
            return
        try:
            self._overwrite_app()
            self._restart()
        except ClientError as err:
            log.error(str(err), exc_info=True)

    def _get_update_manifest(self):
        #  Downloads & Verifies version file signature.
        log.debug(u'Loading version file...')
        try:
            v = requests.get(self.version_url, verify=self.verify)
            self.json_data = v.json()
        except requests.exceptions.SSLError:
                log.error(u'SSL cert not verified')
                raise ClientError(u'SSL cert not verified')
        except ValueError:
            log.error(u'Json failed to load')
            raise ClientError(u'Failed to load json')
        except Exception as e:
            log.error(str(e))
        finally:
            if self.json_data is None:
                self.json_data = {}

        # Checking to see if there is a sig in the version file.
        if u'sig' in self.json_data.keys():
            self.sig = self.json_data[u'sig']
            log.debug(u'Deleting sig from update data')
            del self.json_data[u'sig']

            # After removing the sig we turn the json data back
            # into a string to use as data to verify the sig.
            update_data = json.dumps(self.json_data, sort_keys=True)

            # I added this try/except block because sometimes a
            # None value in json_data would find its way down here.
            # Hopefully i fixed it by return right under the Exception
            # block above.  But just in case will leave anyway.
            try:
                result = rsa_verify(update_data, self.sig, self.public_key)
            except Exception as e:
                log.error(str(e))
                result = False
            if result:
                log.debug(u'Version file verified')
                self.verified = True

            else:
                self.json_data = None
                log.warning(u'Version file not verified')
        else:
            log.error(u'No sig in version file')
        self.dot_access_update_data = DotAccessDict(self.json_data)

    def _extract_update(self):
        platform_name = self.name
        if sys.platform == u'win32' and self.name == self.app_name:
            # We only add .exe to app executable.  Not libs or dll
            log.debug(u'Adding .exe to filename for windows main app udpate.')
            platform_name += u'.exe'
        latest = self._get_highest_version(self.name)
        filename = self._get_filename(self.name,
                                      latest)

        with ChDir(self.update_folder):
            if not os.path.exists(filename):
                raise ClientError(u'File does not exists')

            log.info(u'Extracting Update')
            archive_ext = os.path.splitext(filename)[1].lower()
            if archive_ext == u'.gz':
                try:
                    with tarfile.open(filename, u'r:gz') as tfile:
                        # Extract file update to current
                        # directory.
                        tfile.extractall()
                except Exception as err:
                    log.error(err, exc_info=True)
                    raise ClientError(u'Error reading gzip file')
            elif archive_ext == u'.zip':
                try:
                    with ZipFile(filename, u'r') as zfile:
                        # Extract update file to current
                        # directory.
                        zfile.extractall()
                except Exception as err:
                    log.error(err, exc_info=True)
                    raise ClientError(u'Error reading zip file')
            else:
                raise ClientError(u'Unknown filetype')

    def _overwrite_app(self):
        # Unix: Overwrites the running applications binary,
        #       then starts the updated binary in the currently
        #       running applications process memory.
        # Windows: Moves update to current directory of running
        #          application then restarts application using
        #          new update.
        current_app = os.path.join(self.current_app_dir, self.name)
        app_update = os.path.join(self.update_folder, self.name)
        log.debug(u'Current App location:\n\n{}'.format(current_app))
        log.debug(u'Update Location:\n\n{}'.format(app_update))

        if get_system() == u'mac':
            if not os.path.exists(app_update):
                app_update += u'.app'

        if os.path.exists(current_app):
            os.remove(current_app)
        if os.path.exists(current_app + u'.app'):
            shutil.rmtree(current_app + u'.app', ignore_errors=True)

        log.debug(u'Moving app to new location')
        shutil.move(app_update, os.path.dirname(current_app))

    def _restart(self):
        # Oh yes i did just pull that new binary into
        # the currently running process and kept it pushing
        # like nobody's business. Windows what???
        log.info(u'Restarting')
        current_app = os.path.join(self.current_app_dir, self.name)
        if get_system() == u'mac':
            if not os.path.exists(current_app):
                current_app += u'.app'
                mac_app_binary_dir = os.path.join(current_app, u'Contents',
                                                  u'MacOS')
                current_app = os.path.join(mac_app_binary_dir, self.name)

        os.execv(current_app, [current_app])

    def _win_overwrite_app_restart(self):
        # Pretty much went through this work to show love to
        # all platforms.  But sheeeeesh!
        current_app = os.path.join(self.current_app_dir, self.name)
        updated_app = os.path.join(self.update_folder, self.name)
        current_app += u'.exe'
        updated_app += u'.exe'
        bat = os.path.join(self.current_app_dir, u'update.bat')
        with open(bat, u'w') as batfile:
            # Not sure whats going on here.  Next time will
            # def link the article in these comments :)
            if ' ' in current_app:
                fix = '""'
            else:
                fix = ''
            # Now i'm back to understanding
            batfile.write(u"""
@echo off
echo Updating to latest version...
ping 127.0.0.1 -n 5 -w 1000 > NUL
move /Y "{}" "{}" > NUL
echo restarting...
start {} "{}" """.format(updated_app, current_app, fix, current_app))
        log.debug(u'Starting bat file')
        os.startfile(bat)
        sys.exit(0)

    def _setup(self):
        # Sets up required directories on end-users computer
        # to place verified update data
        # Very safe director maker :)
        log.debug(u'Setting up directories...')
        dirs = [self.data_dir, self.update_folder]
        for d in dirs:
            if not os.path.exists(d):
                log.debug(u'Creating directory: {}'.format(d))
                os.makedirs(d)

    def _patch_update(self, name, version):
        # Updates the binary by patching
        #
        # Args:
        #    name (str): Name of file to update
        #
        #     version (str): Current version number of file to update
        #
        # Returns:
        #    (bool) Meanings::
        #
        #        True - Either already up to date or patched successful
        #
        #        False - Either failed to patch or no base binary to patch

        log.info(u'Starting patch update')
        filename = self._get_filename(name, version)
        latest = self._get_highest_version(name)
        # Just checking to see if the zip for the current version is
        # available to patch If not we'll just do a full binary download
        if not os.path.exists(os.path.join(self.update_folder, filename)):
            log.warning(u'{} got deleted. No base binary to start patching '
                        'form'.format(filename))
            return False

        p = Patcher(name=name, json_data=self.json_data,
                    current_version=version, highest_version=latest,
                    update_folder=self.update_folder,
                    update_url=self.update_url, verify=self.verify)

        # Returns True if everything went well
        # If False is returned then we will just do the full
        # update.
        return p.start()

    def _full_update(self, name):
        # Updates the binary by downloading full update
        #
        # Args:
        #    name (str): Name of file to update
        #
        #    version (str): Current version number of file to update
        #
        # Returns:
        #    (bool) Meanings::
        #
        #       True - Update Successful
        #
        #       False - Update Failed
        log.info(u'Starting full update')
        latest = self._get_highest_version(name)

        filename = self._get_filename(name,
                                      latest)

        url = self.update_url + filename
        hash_key = u'{}.{}.{}.{}.{}'.format(self.updates_key, name,
                                            latest, platform_, u'file_hash')
        _hash = self.dot_access_update_data.get(hash_key)

        with ChDir(self.update_folder):
            log.info(u'Downloading update...')
            fd = FileDownloader(filename, url, _hash, self.verify)
            result = fd.download_verify_write()
            if result:
                log.info(u'Update Complete')
                return True
            else:
                log.error(u'Failed To Updated To Latest Version')
                return False

    def _archive_installed_binary(self):
        # Archives current app and places in cache for future patch updates

        current_archive_filename = self._get_filename(self.name, self.version)

        current_archvie_path = os.path.join(self.update_folder,
                                            current_archive_filename)

        if not os.path.exists(current_archvie_path):
            log.info(u'Adding base binary v{} to updates '
                     u'folder'.format(self.version))
            # Changing in to directory of currently running exe
            with ChDir(os.path.dirname(sys.argv[0])):
                name = self.name
                if get_system() == u'win':
                    name += u'.exe'
                if get_system() == u'mac':
                    # If not found must be a mac gui app
                    if not os.path.exists(name):
                        name += u'.app'

                archive_ext = os.path.splitext(current_archive_filename)[1]
                if u'gz' in archive_ext:
                    archive_format = u'gztar'
                else:
                    archive_format = u'zip'

                try:
                    plat = get_system()
                    filename = make_archive(self.name, self.version, name,
                                            archive_format, platfrom=plat)
                except Exception as err:
                    filename = None
                    log.error(str(err), exc_info=True)

                if filename is not None:
                    shutil.move(filename, self.update_folder)

    def _remove_old_updates(self):
        # Removes old updates from cache. Patch updates
        # start from currently installed version.

        # ToDo: Better filename comparison
        #       Please chime in if this is sufficient
        #       Will remove todo if so...
        temp = os.listdir(self.update_folder)
        try:
            filename = self._get_filename(self.name, self.version)
        except KeyError:
            filename = u'0.0.0'

        try:
            current_version_str = get_version_number(filename)
        except UtilsError:
            log.warning(u'Cannot parse version info')
            current_version_str = u'0.0.0'

        current_version = version_string_to_tuple(current_version_str)
        with ChDir(self.update_folder):
            for t in temp:
                try:
                    t_versoin_str = get_version_number(t)
                except UtilsError:
                    log.warning(u'Cannot parse version info')
                    t_versoin_str = u'0.0.0'
                t_version = version_string_to_tuple(t_versoin_str)

                if self.name in t and t_version < current_version:
                    log.debug(u'Removing old update: {}'.format(t))
                    os.remove(t)

    def _get_highest_version(self, name):
        # Parses version file and returns the highest version number.
        #
        # Args:
        #    name (str): name of file to search for updates
        #
        # Returns:
        #    (str) Highest version number
        version_key = u'{}.{}.{}'.format(u'latest', name, platform_)

        version = self.dot_access_update_data.get(version_key)

        if version is not None:
            log.debug(u'Highest version: {}'.format(version))
        else:
            log.error(u'No updates named "{}" exists'.format(name))
        return version

    def _get_new_update_url(self, name):
        # Returns url for given name & version combo
        #
        # Args:
        #    name (str): name of file to get url for
        #
        #    version (str): version of file to get url for
        #
        # Returns:
        #    (str) Url
        latest_key = u'{}.{}.{}'.format(u'latest', name, platform_)
        latest = self.dot_access_update_data.get(latest_key)

        url_key = u'{}.{}.{}.{}.{}'.format(self.updates_key, name, latest,
                                           platform_, u'url')
        url = self.dot_access_update_data.get(url_key)
        return url

    def _get_filename(self, name, version):
        # Gets full filename for given name & version combo
        #
        #Args:
        #    name (str): name of file to get full filename for
        #
        #    version (str): version of file to get full filename for
        #
        #Returns:
        #    (str) Filename with extension

        # ToDo: Remove once stable.  Used to help with transition
        #       to new version file format.
        filename_key = u'{}.{}.{}.{}.{}'.format(u'updates', name, version,
                                                platform_, u'filename')
        filename = self.dot_access_update_data.get(filename_key)

        log.debug(u"Filename for {}-{}: {}".format(name, version, filename))
        return filename

    def _fix_update_url(self, url):
        # Adds trailing slash to urls provided in config if
        # not already present
        #
        # Args:
        #    url (str): url to process
        #
        # Returns:
        #    (str) Url with trailing slash

        # Adds trailing slash to end of url
        # if not already provided
        if not url.endswith(u'/'):
            return url + u'/'
        return url
