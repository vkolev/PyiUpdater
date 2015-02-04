# --------------------------------------------------------------------------
# Copyright 2014 Digital Sapphire Development Team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# --------------------------------------------------------------------------
import gzip
import json
import logging
import os
import shutil

from appdirs import user_data_dir, user_cache_dir
import certifi
import ed25519
from jms_utils import FROZEN
from jms_utils.logger import log_format_string
from jms_utils.paths import app_cwd, ChDir
from jms_utils.system import get_system
import six
import urllib3

from pyi_updater.client.updates import AppUpdate, LibUpdate
from pyi_updater.config import PyiUpdaterConfig
from pyi_updater.downloader import FileDownloader
from pyi_updater import settings
from pyi_updater.utils import (convert_to_list,
                               EasyAccessDict,
                               get_highest_version,
                               gzip_decompress,
                               Version)

log = logging.getLogger(__name__)

if os.path.exists(os.path.join(app_cwd, u'pyiu.log')):
    ch = logging.FileHandler(os.path.join(app_cwd, u'pyiu.log'))
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(log_format_string())
    log.addHandler(ch)


class Client(object):
    """Used on client side to update files

    Kwargs:

        obj (instance): config object

        refresh (bool) Meaning:

            True: Refresh update manifest on object initialization

            False: Don't refresh update manifest on object initialization

        call_back (func): Used for download progress
    """

    def __init__(self, obj=None, refresh=False, call_back=None, test=False):
        self.name = None
        self.version = None
        self.json_data = None
        self.verified = False
        self.ready = False
        self.progress_hooks = []
        if call_back is not None:
            self.progress_hooks.append(call_back)
        self.init_app(obj, refresh, test)

    def init_app(self, obj, refresh=False, test=False):
        """Sets up client with config values from obj

        Args:

            obj (instance): config object

        """
        # Used to add missing required information
        # i.e. APP_NAME
        pyi_config = PyiUpdaterConfig(obj)
        config = pyi_config.copy()

        # Grabbing config information
        update_url = config.get(u'UPDATE_URL')
        update_urls = config.get(u'UPDATE_URLS')

        self.update_urls = self._sanatize_update_url(update_url, update_urls)
        self.app_name = config.get(u'APP_NAME', u'PyiUpdater')
        self.company_name = config.get(u'COMPANY_NAME', u'Digital Sapphire')
        if test:
            self.data_dir = 'cache'
            self.platform = 'mac'
        else:
            # ToDo: Remove v0.19
            old_dir = user_cache_dir(self.app_name, self.company_name)
            if os.path.exists(old_dir):
                shutil.rmtree(old_dir, ignore_errors=True)
            # End ToDo
            self.data_dir = user_data_dir(self.app_name, self.company_name,
                                          roaming=True)
            self.platform = get_system()
        self.update_folder = os.path.join(self.data_dir,
                                          settings.UPDATE_FOLDER)
        self.public_keys = convert_to_list(config.get(u'PUBLIC_KEYS'),
                                           default=list())
        if len(self.public_keys) == 0:
            log.warning(u'May have pass an incorrect data type to PUBLIC_KEYS')
        # ToDo: Remove in v1.0
        if config.get(u'PUBLIC_KEY') is not None:
            pub_key = convert_to_list(config.get(u'PUBLIC_KEY'),
                                      default=list())
            if len(pub_key) == 0:
                log.warning(u'May have pass an incorrect data type '
                            u'to PUBLIC_KEY')
            self.public_keys += pub_key
        # Sometimes a little bit goes a long way
        self.public_keys = list(set(self.public_keys))
        self.verify = config.get(u'VERIFY_SERVER_CERT', True)
        if self.verify is True:
            self.http_pool = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                                                 ca_certs=certifi.where())
        else:
            self.http_pool = urllib3.PoolManager()
        self.version_file = settings.VERSION_FILE

        self._setup()
        if refresh is True:
            self.refresh()

    def refresh(self):
        """Will download and verify your updates version file.

        Proxy method from :meth:`_get_update_manifest`.
        """
        try:
            self._get_update_manifest()
        except Exception as err:
            log.debug(str(err), exc_info=True)
            log.error(str(err))

    def update_check(self, name, version):
        """
        Will try to patch binary if all check pass.  IE hash verified
        signature verified.  If any check doesn't pass then falls back to
        full update

        Args:

            name (str): Name of file to update

            version (str): Current version number of file to update

        Returns:

            (bool) Meanings:

                True - Update Successful

                False - Update Failed
        """
        self.name = name
        version = Version(version)
        self.version = str(version)

        app = False
        if self.ready is False:
            log.warning('No update manifest found')
            return None
        if FROZEN is True and self.name == self.app_name:
            app = True
        # Checking if version file is verified before
        # processing data contained in the version file.
        # This was done by self._get_update_manifest()
        if self.verified is False:
            log.error('Failed version file verification')
            return None
        log.info(u'Checking for {} updates...'.format(name))

        # If None is returned self._get_highest_version could
        # not find the supplied name in the version file
        latest = get_highest_version(name, self.platform,
                                     self.easy_data)
        if latest is None:
            return None
        latest = Version(latest)
        if latest <= version:
            log.info(u'{} already updated to the latest version'.format(name))
            return None
        # Hey, finally made it to the bottom!
        # Looks like its time to do some updating
        log.info(u'Update available')
        data = {
            u'update_urls': self.update_urls,
            u'name': self.name,
            u'version': self.version,
            u'easy_data': self.easy_data,
            u'json_data': self.json_data,
            u'data_dir': self.data_dir,
            u'platform': self.platform,
            u'app_name': self.app_name,
            u'verify': self.verify,
            u'progress_hooks': self.progress_hooks,
            }
        if app is True:
            return AppUpdate(data)
        else:
            return LibUpdate(data)

    def add_call_back(self, cb):
        self.progress_hooks.append(cb)

    def _get_manifest_filesystem(self):
        with ChDir(self.data_dir):
            if not os.path.exists(self.version_file):
                log.warning('No version file on file system')
                return None
            else:
                log.info('Found version file on file system')
                try:
                    with open(self.version_file, u'rb') as f:
                        data = f.read()
                    log.info('Loaded version file from file system')
                except Exception as err:
                    log.error('Failed to load version file from file '
                              u'system')
                    log.debug(str(err), exc_info=True)
                    data = None

                return gzip_decompress(data)

    def _download_manifest(self):
        log.info('Downloading online version file')
        try:
            fd = FileDownloader(self.version_file, self.update_urls)
            data = fd.download_verify_return()
            log.info('Version file download successful')
            decompressed_data = gzip_decompress(data)
            self._write_manifest_2_filesystem(decompressed_data)
            return decompressed_data
        except Exception as err:
            log.error('Version file failed to download')
            log.debug(str(err), exc_info=True)
            return None

    def _write_manifest_2_filesystem(self, data):
        with ChDir(self.data_dir):
            log.debug('Writing version file to disk')
            with gzip.open(self.version_file, u'wb') as f:
                f.write(data)

    def _get_update_manifest(self):
        #  Downloads & Verifies version file signature.
        log.info(u'Loading version file...')

        data = self._download_manifest()
        if data is None:
            data = self._get_manifest_filesystem()

        try:
            log.debug('Data type: {}'.format(type(data)))
            self.json_data = json.loads(data)
            self.ready = True
        except ValueError as err:
            log.debug(str(err), exc_info=True)
            log.error(u'Json failed to load: ValueError')
        except Exception as err:
            # Catch all for debugging purposes.
            # If seeing this line come up a lot in debug logs
            # please open an issue on github or submit a pull request
            log.error(str(err))
            log.debug(str(err), exc_info=True)

        if self.json_data is None:
            self.json_data = {}

        self.json_data = self._verify_sig(self.json_data)

        self.easy_data = EasyAccessDict(self.json_data)
        log.debug('Version Data:\n{}'.format(str(self.easy_data)))

    def _verify_sig(self, data):
        # Checking to see if there is a sig in the version file.
        if u'sigs' in data.keys():
            signatures = data[u'sigs']
            # ToDo: Remove in v1.0: Fix for migragtion & tests
            if u'sig' in data.keys():
                log.debug(u'Deleting sig from update data')
                del data[u'sig']
            log.debug(u'Deleting sigs from update data')
            del data[u'sigs']

            # After removing the sig we turn the json data back
            # into a string to use as data to verify the sig.
            update_data = json.dumps(data, sort_keys=True)

            for pk in self.public_keys:
                log.debug(u'Public Key: {}'.format(pk))
                for s in signatures:
                    log.debug(u'Signature: {}'.format(s))
                    # I added this try/except block because sometimes a
                    # None value in json_data would find its way down here.
                    # Hopefully i fixed it by return right under the Exception
                    # block above.  But just in case will leave anyway.
                    try:
                        pub_key = ed25519.VerifyingKey(pk, encoding='base64')
                        pub_key.verify(s, update_data, encoding='base64')
                    except Exception as err:
                        log.error(str(err))
                    else:
                        log.info(u'Version file verified')
                        self.verified = True
                        break
                if self.verified is True:
                    # No longer need to iterate through public keys
                    break
            else:
                log.warning(u'Version file not verified')

        else:
            log.warning(u'Version file not verified, no signature found')

        if data is None:
            data = {}
        return data

    def _setup(self):
        # Sets up required directories on end-users computer
        # to place verified update data
        # Very safe director maker :)
        log.info(u'Setting up directories...')
        dirs = [self.data_dir, self.update_folder]
        for d in dirs:
            if not os.path.exists(d):
                log.info(u'Creating directory: {}'.format(d))
                os.makedirs(d)

    def _sanatize_update_url(self, url, urls):
        _urls = []
        if isinstance(url, list):
            log.warning(u'UPDATE_URL value should only be string.')
            _urls += url
        elif isinstance(url, tuple):
            log.warning(u'UPDATE_URL value should only be string.')
            _urls += list(url)
        elif isinstance(url, six.string_types):
            _urls.append(url)
        else:
            log.warning(u'UPDATE_URL should be type "{}" got '
                        u'"{}"'.format(type(''), type(url)))

        if isinstance(urls, list):
            _urls += urls
        elif isinstance(url, tuple):
            _urls += list(url)
        elif isinstance(urls, six.string_types):
            log.warning(u'UPDATE_URLS value should only be a list.')
            _urls.append(urls)
        else:
            log.warning(u'UPDATE_URLS should be type "{}" got '
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
