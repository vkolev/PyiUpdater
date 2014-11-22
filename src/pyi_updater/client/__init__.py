import json
import logging
import os
import shutil
import sys

from appdirs import user_cache_dir
import certifi
import ed25519
from jms_utils import FROZEN
from jms_utils.paths import ChDir
from jms_utils.system import get_system
import urllib3

from pyi_updater.client.update import AppUpdate, LibUpdate
from pyi_updater.client.utils import (get_highest_version,
                                      get_mac_dot_app_dir)
from pyi_updater.config import Config
from pyi_updater.downloader import FileDownloader
from pyi_updater.exceptions import ClientError, UtilsError
from pyi_updater.utils import (EasyAccessDict,
                               make_archive,
                               version_string_to_tuple)

log = logging.getLogger(__name__)


class Client(object):
    """Used on client side to update files

    Kwargs:

        obj (instance): config object
    """

    def __init__(self, obj=None, test=False):
        self.name = None
        self.version = None
        self.json_data = None
        self.verified = False
        self.ready = False
        self.updates_key = u'updates'
        if obj:
            self.init_app(obj, test)
        if obj is None and test is True:
            self.init_app(None, test)

    def init_app(self, obj, test=False):
        """Sets up client with config values from obj

        Args:
            obj (instance): config object

        """
        # ToDo: Remove once code is v1.0
        #       Updated how client is initialized.  Can still be
        #       used the old way but the new way is way more efficient
        #       Just pass in the config object and the client takes care
        #       of the rest.  No need to initialize PyiUpater object first!
        if hasattr(obj, 'config'):
            config = obj.config.copy()
        else:
            config = Config()
            config.from_object(obj)

        # Grabbing config information
        update_url = config.get(u'UPDATE_URL', None)
        update_urls = config.get(u'UPDATE_URLS', None)

        self.update_urls = self._sanatize_update_url(update_url, update_urls)
        self.app_name = config.get(u'APP_NAME', u'PyiUpdater')
        self.company_name = config.get(u'COMPANY_NAME', u'Digital Sapphire')
        if test:
            self.data_dir = 'cache'
            self.platform = 'mac'
        else:
            self.data_dir = user_cache_dir(self.app_name, self.company_name)
            self.platform = get_system()
        self.update_folder = os.path.join(self.data_dir, u'update')
        self.public_key = config.get(u'PUBLIC_KEY', None)
        self.debug = config.get(u'DEBUG', False)
        self.verify = config.get(u'VERIFY_SERVER_CERT', True)
        if self.verify is True:
            self.http_pool = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                                                 ca_certs=certifi.where())
        else:
            self.http_pool = urllib3.PoolManager()
        self.version_file = u'version.json'

        self.current_app_dir = os.path.dirname(sys.argv[0])

        self._setup()

    def refresh(self):
        """Will download and verify your updates version file.

        Proxy method from :meth:`_get_update_manifest`.
        """
        try:
            return self._get_update_manifest()
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
        if self.ready is False:
            log.debug('No update manifest found')
            return None
        if FROZEN is True and self.name == self.app_name:
            app = True
            self._archive_installed_binary()

        # Checking if version file is verified before
        # processing data contained in the version file.
        # This was done by self._get_update_manifest()
        if not self.verified:
            log.debug('Failed version file verification')
            return None
        log.debug(u'Checking for {} updates...'.format(name))

        # If None is returned self._get_highest_version could
        # not find the supplied name in the version file
        latest = get_highest_version(name, self.platform,
                                     self.star_access_update_data)
        if latest is None:
            return None
        if version_string_to_tuple(latest) <= \
                version_string_to_tuple(version):
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
            u'easy_data': self.star_access_update_data,
            u'data_dir': self.data_dir,
            u'platform': self.platform,
            u'app_name': self.app_name,
            }
        if app is True:
            return AppUpdate(data)
        else:
            return LibUpdate(data)

    def _get_manifest_filesystem(self):
        with ChDir(self.data_dir):
            if not os.path.exists(self.version_file):
                return None
            else:
                try:
                    with open(self.version_file, u'r') as f:
                        data = f.read()
                except Exception as err:
                    log.debug(str(err))
                    data = None

                return data

    def _get_manifest_online(self):
        try:
            fd = FileDownloader(self.version_file, self.update_urls)
            data = fd.download_verify_return()
            return data
        except Exception as err:
            log.debug(str(err))
            return None

    def _write_manifest_2_filesystem(self, data):
        with ChDir(self.data_dir):
            with open(self.version_file, u'w') as f:
                f.write(data)

    def _get_update_manifest(self):
        #  Downloads & Verifies version file signature.
        log.debug(u'Loading version file...')

        data = self._get_manifest_online()
        if data is None:
            data = self._get_manifest_filesystem()
        else:
            self._write_manifest_2_filesystem(data)

        if data is None:
            return False

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
                pub_key = ed25519.VerifyingKey(self.public_key,
                                               encoding='base64')
                pub_key.verify(self.sig, update_data, encoding='base64')
            except Exception as e:
                log.error(str(e))
                self.json_data = None
                log.debug(u'Version file not verified')
            else:
                log.debug(u'Version file verified')
                self.verified = True

        else:
            log.error(u'No sig in version file')

        if self.json_data is None:
            j_data = {}
        else:
            j_data = self.json_data.copy()
        self.star_access_update_data = EasyAccessDict(j_data)
        return True

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

        current_archive_filename = self._get_filename(self.name, self.version)

        current_archvie_path = os.path.join(self.update_folder,
                                            current_archive_filename)

        if not os.path.exists(current_archvie_path):
            log.debug(u'Adding base binary v{} to updates '
                      u'folder'.format(self.version))
            # Changing in to directory of currently running exe

            if get_system() == u'mac':
                # We are in an application bundle. Must get parent
                # dir of bundle.
                if self.current_app_dir.endswith('MacOS') is True:
                    log.debug('Looks like we\'re dealing with a Mac Gui')
                    p_dir = get_mac_dot_app_dir(self.current_app_dir)
                else:
                    p_dir = os.path.dirname(sys.agrv[0])
            else:
                p_dir = os.path.dirname(sys.agrv[0])

            with ChDir(p_dir):
                name = self.name
                if get_system() == u'win':
                    name += u'.exe'
                if get_system() == u'mac':
                    # If not found must be a mac gui app
                    if not os.path.exists(name):
                        name += u'.app'

                try:
                    filename = make_archive(self.name, self.version, name)
                except Exception as err:
                    filename = None
                    log.error(str(err), exc_info=True)

                if filename is not None:
                    shutil.move(filename, self.update_folder)
