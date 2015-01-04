#--------------------------------------------------------------------------
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
#--------------------------------------------------------------------------

import json
import logging
import os
import shutil

from appdirs import user_cache_dir
import certifi
import ed25519
from jms_utils import FROZEN
from jms_utils.logger import log_format_string
from jms_utils.paths import app_cwd, ChDir
from jms_utils.system import get_system
import six
import urllib3

from pyi_updater.client.updates import AppUpdate, LibUpdate
from pyi_updater.client.utils import (convert_to_list,
                                      get_filename,
                                      get_highest_version)
from pyi_updater.config import PyiUpdaterConfig
from pyi_updater.downloader import FileDownloader
from pyi_updater import settings
from pyi_updater.utils import (EasyAccessDict,
                               make_archive,
                               vstr_2_vtuple)

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
    """

    def __init__(self, obj=None, refresh=False, test=False):
        self.name = None
        self.version = None
        self.json_data = None
        self.verified = False
        self.ready = False
        if obj and test is True:
            self.init_app(obj, refresh, test)

        if obj and test is False:
            self.init_app(obj, refresh, test)

    def init_app(self, obj, refresh=True, test=False):
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
            self.data_dir = user_cache_dir(self.app_name, self.company_name)
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
        self._setup()
        try:
            self._get_update_manifest()
        except Exception as err:
            log.debug(str(err), exc_info=True)

    def _sanatize_version_to_str(self, version):
        def length_check(v):
            if len(v) == 1:
                v = (v[0], 0, 0)
            elif len(v) == 2:
                v = (v[0], v[1], 0)
            # ToDo: Once we add support for pre release versions
            #       We will have to update this. Can't fix now.
            #       Have bigger fish to fry. 2014/12/7 6:51pm
            elif len(v) > 3:
                v = (v[0], v[1], v[2])
            return v

        if isinstance(version, tuple):
            version = length_check(version)
            version = '.'.join(map(str, version))
        elif isinstance(version, list):
            version = tuple(map(int, version.split('.')))
            version = length_check(version)
            version = '.'.join(version)

        return version

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
        self.version = self._sanatize_version_to_str(version)

        app = False
        if self.ready is False:
            log.debug('No update manifest found')
            return None
        if FROZEN is True and self.name == self.app_name:
            app = True
            self._archive_installed_binary()

        # Checking if version file is verified before
        # processing data contained in the version file.
        # This was done by self._get_update_manifest()
        if self.verified is False:
            log.debug('Failed version file verification')
            return None
        log.debug(u'Checking for {} updates...'.format(name))

        # If None is returned self._get_highest_version could
        # not find the supplied name in the version file
        latest = get_highest_version(name, self.platform,
                                     self.easy_data)
        if latest is None:
            return None
        if vstr_2_vtuple(latest) <= \
                vstr_2_vtuple(version):
            log.debug(u'{} already updated to the latest version'.format(name))
            log.debug(u'Already up-to-date')
            return None
        # Hey, finally made it to the bottom!
        # Looks like its time to do some updating
        log.debug(u'Update available')
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
            }
        if app is True:
            return AppUpdate(data)
        else:
            return LibUpdate(data)

    def _get_manifest_filesystem(self):
        with ChDir(self.data_dir):
            if not os.path.exists(self.version_file):
                log.debug('No version file on file system')
                return None
            else:
                log.debug('Found version file on file system')
                try:
                    with open(self.version_file, u'r') as f:
                        data = f.read()
                    log.debug('Loaded version file from file system')
                except Exception as err:
                    log.debug('Failed to load version file from file system')
                    log.debug(str(err))
                    data = None

                return data

    def _download_manifest(self):
        log.debug('Downloading online version file')
        try:
            fd = FileDownloader(self.version_file, self.update_urls)
            data = fd.download_verify_return()
            return data
            self._write_manifest_2_filesystem(data)
            log.debug('Version file download successful')
        except Exception as err:
            log.debug('Version file failed to download')
            log.debug(str(err))
            return None

    def _write_manifest_2_filesystem(self, data):
        with ChDir(self.data_dir):
            with open(self.version_file, u'w') as f:
                f.write(data)

    def _get_update_manifest(self):
        #  Downloads & Verifies version file signature.
        log.debug(u'Loading version file...')

        data = self._download_manifest()
        if data is None:
            data = self._get_manifest_filesystem()

        try:
            log.debug('Data type: {}'.format(type(data)))
            self.json_data = json.loads(data)
            self.ready = True
        except ValueError:
            log.error(u'Json failed to load')
        except Exception as e:
            # Catch all for debugging purposes.
            # If seeing this line come up a lot in debug logs
            # please open an issue on github or submit a pull request
            log.error(str(e))

        if self.json_data is None:
            self.json_data = {}

        self.json_data = self._verify_sig(self.json_data)

        self.easy_data = EasyAccessDict(self.json_data)

    def _verify_sig(self, data):
        # Checking to see if there is a sig in the version file.
        if u'sigs' in data.keys():
            signatures = data[u'sigs']
            log.debug(u'Deleting sig from update data')
            # ToDo: Remove in v1.0: Fix for migragtion & tests
            if u'sig' in data.keys():
                del data[u'sig']
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
                    except Exception as e:
                        log.error(str(e))
                        data = None
                    else:
                        log.debug(u'Version file verified')
                        self.verified = True
                        break
                if self.verified is True:
                    # No longer need to iterate through public keys
                    break
            else:
                log.debug(u'Version file not verified')

        else:
            log.error(u'Version file not verified, no signature found')

        if data is None:
            data = {}
        return data

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

    def _archive_installed_binary(self):
        # Archives current app and places in cache for future patch updates

        current_archive_filename = get_filename(self.name, self.version,
                                                self.platform, self.easy_data)

        if current_archive_filename is None:
            current_archive_filename = ''
        current_archvie_path = os.path.join(self.update_folder,
                                            current_archive_filename)

        if current_archive_filename != '' and \
                not os.path.exists(current_archvie_path):
            log.debug(u'Adding base binary v{} to updates '
                      u'folder'.format(self.version))
            # Changing in to directory of currently running exe
            p_dir = app_cwd

            with ChDir(p_dir):
                name = self.name
                if get_system() == u'win':
                    name += u'.exe'
                if get_system() == u'mac':
                    # If not found must be a mac gui app
                    if not os.path.exists(name):
                        name += u'.app'

                try:
                    filename = make_archive(self.name, self.version,
                                            name)
                except Exception as err:
                    filename = None
                    log.error(str(err), exc_info=True)

                if filename is not None:
                    shutil.move(filename, self.update_folder)

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
