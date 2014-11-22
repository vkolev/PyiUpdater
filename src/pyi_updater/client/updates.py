import logging
import os
import shutil
import sys
import tarfile
import warnings
from zipfile import ZipFile

import certifi
from jms_utils.paths import ChDir
from jms_utils.system import get_system
import urllib3
import six

from pyi_updater.client.utils import (get_highest_version,
                                      get_mac_dot_app_dir)
from pyi_updater.downloader import FileDownloader
from pyi_updater.exceptions import ClientError, UtilsError
from pyi_updater.patcher import Patcher
from pyi_updater.utils import (get_hash, get_version_number,
                               version_string_to_tuple)

log = logging.getLogger(__name__)


class LibUpdate(object):
    """Used on client side to update files

    Kwargs:

        obj (instance): config object
    """

    def __init__(self, data):
        self.update_urls = data.get(u'update_urls')
        self.name = data.get(u'name')
        self.version = data.get(u'version')
        self.easy_data = data.get(u'easy_data')
        self.data_dir = data.get(u'data_dir')
        self.platform = data.get(u'platform')
        self.app_name = data.get(u'app_name')
        self.update_folder = os.path.join(self.data_dir, u'updates')
        self.verify = data.get(u'VERIFY_SERVER_CERT')
        if self.verify is True:
            self.http_pool = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                                                 ca_certs=certifi.where())
        else:
            self.http_pool = urllib3.PoolManager()

    def is_downloaded(self):
        if self.name is None:
            return False
        return self._is_downloaded(self.name)

    def download(self):
        """Will download the package update that was referenced
        with check update.

        Proxy method for :meth:`_patch_update` & :meth:`_full_update`.

        Returns:
            (bool) Meanings::

                True - Download successful

                False - Download failed
        """
        if self.name is not None:
            if self._is_downloaded(self.name) is True:
                return True

        patch_success = self._patch_update(self.name, self.version)
        if patch_success:
            log.debug(u'Download successful')
        else:
            update_success = self._full_update(self.name)
            if update_success:
                log.debug(u'Download successful')
            else:
                return False
        # Removes old versions, of update being checked, from
        # updates folder.  Since we only start patching from
        # the current binary this shouldn't be a problem.
        self._remove_old_updates()
        return True

    def extract(self):
        """Will extract archived update and leave in update folder.
            If updating a lib you can take over from there. If updating
            an app this call should be followed by :meth:`restart` to
            complete update.

            Proxy method for :meth:`_extract_update`.

            Returns:
                (bool) Meanings::

                    True - Install successful

                    False - Install failed
        """
        if get_system() == u'win':
            log.debug('Only supported on Unix like systems')
            return False
        try:
            self._extract_update()
        except ClientError as err:
            log.error(str(err), exc_info=True)
            return False
        return True

    def install(self):
        warnings.warn('Will be removed in v1.0, use the extract method',
                      DeprecationWarning)
        self.extract()

    def _extract_update(self):
        with ChDir(self.update_folder):
            platform_name = self.name
            if sys.platform == u'win32' and self.name == self.app_name:
                # We only add .exe to app executable.  Not libs or dll
                log.debug(u'Adding .exe to filename for windows main '
                          'app udpate.')
                platform_name += u'.exe'

            latest = get_highest_version(self.name)
            filename = self._get_filename(self.name,
                                          latest)
            if not os.path.exists(filename):
                raise ClientError(u'File does not exists')

            log.debug(u'Extracting Update')
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

    def _is_downloaded(self, name):
        latest = get_highest_version(name, self.platform, self.easy_data)

        filename = self._get_filename(name,
                                      latest)

        hash_key = u'{}*{}*{}*{}*{}'.format(self.updates_key, name,
                                            latest, self.platform,
                                            u'file_hash')
        _hash = self.easy_data.get(hash_key)
        with ChDir(self.update_folder):
            if not os.path.exists(filename):
                return False
            with open(filename, u'rb') as f:
                data = f.read()
            if _hash == get_hash(data):
                return True
            else:
                return False

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

        log.debug(u'Starting patch update')
        filename = self._get_filename(name, version)
        latest = get_highest_version(name, self.platform,
                                     self.easy_data)
        # Just checking to see if the zip for the current version is
        # available to patch If not we'll just do a full binary download
        if not os.path.exists(os.path.join(self.update_folder, filename)):
            log.debug(u'{} got deleted. No base binary to start patching '
                      'form'.format(filename))
            return False

        p = Patcher(name=name, json_data=self.json_data,
                    current_version=version, highest_version=latest,
                    update_folder=self.update_folder,
                    update_urls=self.update_urls, verify=self.verify)

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
        log.debug(u'Starting full update')
        latest = get_highest_version(name, self.platform, self.easy_data)

        filename = self._get_filename(name,
                                      latest)

        hash_key = u'{}*{}*{}*{}*{}'.format(self.updates_key, name,
                                            latest, self.platform,
                                            u'file_hash')
        _hash = self.easy_data.get(hash_key)

        with ChDir(self.update_folder):
            log.debug(u'Downloading update...')
            fd = FileDownloader(filename, self.update_urls,
                                _hash, self.verify)
            result = fd.download_verify_write()
            if result:
                log.debug(u'Update Complete')
                return True
            else:
                log.error(u'Failed To Updated To Latest Version')
                return False

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
            log.debug(u'Cannot parse version info')
            current_version_str = u'0.0.0'

        current_version = version_string_to_tuple(current_version_str)
        with ChDir(self.update_folder):
            for t in temp:
                try:
                    t_versoin_str = get_version_number(t)
                except UtilsError:
                    log.debug(u'Cannot parse version info')
                    t_versoin_str = u'0.0.0'
                t_version = version_string_to_tuple(t_versoin_str)

                if self.name in t and t_version < current_version:
                    log.debug(u'Removing old update: {}'.format(t))
                    os.remove(t)

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
        latest_key = u'{}*{}*{}'.format(u'latest', name, self.platform)
        latest = self.easy_data.get(latest_key)

        url_key = u'{}*{}*{}*{}*{}'.format(self.updates_key, name, latest,
                                           self.platform, u'url')
        url = self.easy_data.get(url_key)
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
        filename_key = u'{}*{}*{}*{}*{}'.format(u'updates', name, version,
                                                self.platform, u'filename')
        filename = self.easy_data.get(filename_key)

        log.debug(u"Filename for {}-{}: {}".format(name, version, filename))
        return filename

    def _sanatize_update_url(self, url, urls):
        _urls = []
        if isinstance(url, list):
            log.debug(u'WARNING UPDATE_URL value should only be string.')
            _urls += url
        elif isinstance(url, tuple):
            log.debug(u'WARNING UPDATE_URL value should only be string.')
            _urls += list(url)
        elif isinstance(url, six.string_types):
            _urls.append(url)
        else:
            log.debug(u'UPDATE_URL should be type "{}" got '
                      u'"{}"'.format(type(''), type(url)))

        if isinstance(urls, list):
            _urls += urls
        elif isinstance(url, tuple):
            _urls += list(url)
        elif isinstance(urls, six.string_types):
            log.debug(u'WARNING UPDATE_URLS value should only be a list.')
            _urls.append(urls)
        else:
            log.debug(u'UPDATE_URLS should be type "{}" got '
                      u'"{}"'.format(type([]), type('')))

        sanatized_urls = []
        # Adds trailing slash to end of url if not already provided.
        # Doing this so when requesting online resources we only
        # need to add the resouce name to the end of the request.
        for u in _urls:
            if not u.endswith(u'/'):
                sanatized_urls.append(u + u'/')
            else:
                sanatized_urls.append(u)
        # Just removing duplicates
        return list(set(sanatized_urls))


class AppUpdate(LibUpdate):
    """Used on client side to update files

    Kwargs:

        obj (instance): config object
    """

    def __init__(self, data):
        super(AppUpdate).__init__(self, data)

    def extract_restart(self):
        """ Will extract (unzip) the update, overwrite the current app,
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

    def install_restart(self):
        warnings.warn('Will be removed in v1.0, use extract_restart',
                      DeprecationWarning)
        self.extract_restart()

    def restart(self):
        """Will overwrite old binary with updated binary and
        restart using the updated binary.

        Proxy method for :meth:`_overwrite_app` & :meth:`_restart`.
        """
        if get_system() == u'win':
            log.debug(u'Only supported on Unix like systems')
            return
        try:
            self._overwrite_app()
            self._restart()
        except ClientError as err:
            log.error(str(err), exc_info=True)

    def _overwrite_app(self):
        # Unix: Overwrites the running applications binary,
        #       then starts the updated binary in the currently
        #       running applications process memory.
        if get_system() == u'mac':
            if self.current_app_dir.endswith('MacOS') is True:
                log.debug('Looks like we\'re dealing with a Mac Gui')
                temp_dir = get_mac_dot_app_dir(self.current_app_dir)
                self.current_app_dir = temp_dir

        app_update = os.path.join(self.update_folder, self.name)
        if not os.path.exists(app_update):
            app_update += u'.app'
        log.debug(u'Update Location'
                  ':\n{}'.format(os.path.dirname(app_update)))
        log.debug(u'Update Name: {}'.format(os.path.basename(app_update)))

        current_app = os.path.join(self.current_app_dir, self.name)
        if not os.path.exists(current_app):
            current_app += u'.app'
        log.debug(u'Current App location:\n\n{}'.format(current_app))
        if os.path.exists(current_app):
            if os.path.isfile(current_app):
                os.remove(current_app)
            else:
                shutil.rmtree(current_app, ignore_errors=True)

        log.debug(u'Moving app to new location')
        shutil.move(app_update, os.path.dirname(current_app))

    def _restart(self):
        # Oh yes i did just pull that new binary into
        # the currently running process and kept it pushing
        # like nobody's business. Windows what???
        log.debug(u'Restarting')
        current_app = os.path.join(self.current_app_dir, self.name)
        if get_system() == u'mac':
            if not os.path.exists(current_app):
                current_app += u'.app'
                mac_app_binary_dir = os.path.join(current_app, u'Contents',
                                                  u'MacOS')
                file_ = os.listdir(mac_app_binary_dir)
                # We are making an assumption here that only 1
                # executable will be in the MacOS folder.
                current_app = os.path.join(mac_app_binary_dir, file_[0])
                log.debug('Mac .app exe path: {}'.format(current_app))

        os.execv(current_app, [self.name])

    def _win_overwrite_app_restart(self):
        # Windows: Moves update to current directory of running
        #          application then restarts application using
        #          new update.
        # Pretty much went through this work to show love to
        # all platforms.  But sheeeeesh!
        exe_name = self.name + u'.exe'
        current_app = os.path.join(self.current_app_dir, exe_name)
        updated_app = os.path.join(self.update_folder, exe_name)

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
start {} "{}"
DEL "%~f0" """.format(updated_app, current_app, fix, current_app))
        log.debug(u'Starting bat file')
        os.startfile(bat)
        sys.exit(0)
