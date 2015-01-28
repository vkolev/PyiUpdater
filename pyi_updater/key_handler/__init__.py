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
from __future__ import print_function
import gzip
import json
import logging
import os
import shutil

from pyi_updater.key_handler.keydb import KeyDB
from pyi_updater import settings
from pyi_updater.utils import lazy_import


log = logging.getLogger(__name__)

six = None
ed25519 = None
jms_utils = None


class KeyHandler(object):
    """KeyHanlder object is used to manage keys used for signing updates

    Kwargs:

        app (obj): Config object to get config values from
    """

    def __init__(self, app=None):
        global six
        global ed25519
        global jms_utils
        six = lazy_import(u'six')
        ed25519 = lazy_import(u'ed25519')
        jms_utils = lazy_import(u'jms_utils')
        self.key_encoding = 'base64'
        if app:
            self.init_app(app)

    def init_app(self, obj):
        """Sets up client with config values from obj

        Args:

            obj (instance): config object
        """
        # Copies and sets all needed config attributes
        # for this object
        self.app_name = obj.get(u'APP_NAME')
        self.private_key_name = self.app_name + u'.pem'
        self.public_key_name = self.app_name + u'.pub'
        data_dir = os.path.abspath(os.getcwd())
        self.config_dir = os.path.join(data_dir, u'.pyiupdater')
        self.keysdb = KeyDB(self.config_dir)
        # ToDo: Remove in v1.0 No longer using keys dir
        self.keys_dir = os.path.join(self.config_dir, u'keys')
        # End ToDo
        self.data_dir = os.path.join(data_dir, settings.USER_DATA_FOLDER)
        self.deploy_dir = os.path.join(self.data_dir, u'deploy')
        self.version_data = os.path.join(self.config_dir,
                                         settings.VERSION_FILE_DB)

        self.old_version_file = os.path.join(self.deploy_dir,
                                             settings.VERSION_FILE_OLD)
        self.version_file = os.path.join(self.deploy_dir,
                                         settings.VERSION_FILE)
        self._migrate()

    def _migrate(self):
        log.info('Migration check...')
        self.keysdb.load()
        pub = os.path.join(self.keys_dir, self.public_key_name)
        pri = os.path.join(self.keys_dir, self.private_key_name)
        if os.path.exists(pub) and os.path.exists(pri):
            log.info('Migrating keys...')
            with open(pub, u'r') as f:
                public = f.read()
            with open(pri, u'r') as f:
                private = f.read()
            self.keysdb.add_key(public, private)
            if os.path.exists(pub):
                os.remove(pub)
            if os.path.exists(pri):
                os.remove(pri)
            if os.path.exists(self.keys_dir):
                shutil.rmtree(self.keys_dir, ignore_errors=True)
            self.make_keys()
        else:
            log.info('Migration not needed')

    def make_keys(self, count=3):
        """Makes public and private keys for signing and verification

        Kwargs:

            count (bool): The number of keys to create.
        """
        log.info(u'Making keys')
        c = 0
        while c < count:
            self._make_keys()
            c += 1

    def _make_keys(self):
        # Makes a set of private and public keys
        # Used for authentication
        self.keysdb.load()
        privkey, pubkey = ed25519.create_keypair()
        pri = privkey.to_ascii(encoding=self.key_encoding)
        pub = pubkey.to_ascii(encoding=self.key_encoding)
        self.keysdb.add_key(pub, pri)

    def sign_update(self):
        """Signs version file with private key

        Proxy method for :meth:`_add_sig`
        """
        # Loads private key
        # Loads version file to memory
        # Signs Version file
        # Writes version file back to disk
        self._add_sig()

    # ToDo: Remove in v1.0
    def get_public_key(self):
        """Returns (object): Public Key
        """
        return self.get_public_keys()

    def get_public_keys(self):
        """Returns (object): Public Key
        """
        self.keysdb.load()
        return self.keysdb.get_public_keys()

    def get_recent_revoked_key(self):
        self.keysdb.load()
        return self.keysdb.get_revoked_key()

    # ToDo: Remove in v1.0
    def print_public_key(self):
        """Prints public key data to console"""
        self.print_public_keys()

    def print_public_keys(self):
        """Prints public key data to console"""
        keys = self.get_public_key()
        print(u'Public Key:\n{}\n\n'.format(keys))

    def revoke_key(self, count):
        self.keysdb.revoke_key(count)
        self.make_keys(count)

    def _load_private_keys(self):
        # Loads private key
        log.debug(u'Loading private key')
        return self.keysdb.get_private_keys()

    def _add_sig(self):
        # Adding new signature to version file
        private_keys = self._load_private_keys()
        # Just making sure we have a least 2 keys so when revoke is
        # called we have a fall back
        if len(private_keys) < 2:
            self.make_keys()
        private_keys = self._load_private_keys()

        update_data = self._load_update_data()
        if u'sigs' in update_data:
            log.debug(u'Removing signatures from version file')
            del update_data[u'sigs']
        update_data_str = json.dumps(update_data, sort_keys=True)

        signatures = list()
        signature = None
        log.info('Creating new signatures to version file')

        # ToDo: Remove in v1.0: Used for migration to v0.14 & above
        old = False
        # ToDo: End
        for p in private_keys:
            if six.PY2 is True and isinstance(p, unicode) is True:
                log.debug('Got type: {}'.format(type(p)))
                p = str(p)
            log.debug(u'Key type: {}'.format(type(p)))
            privkey = ed25519.SigningKey(p, encoding=self.key_encoding)
            sig = privkey.sign(six.b(update_data_str),
                               encoding=self.key_encoding)
            # ToDo: Remove in v1.0: Used for migration to v0.14 & above
            if old is False:
                signature = sig
                old = True
            # ToDo: End
            log.debug('Sig: {}'.format(sig))
            signatures.append(sig)

        og_data = json.loads(update_data_str)
        update_data = og_data.copy()
        update_data[u'sigs'] = signatures
        # ToDo: Remove in v1.0: Used for migration to v0.14 & above
        old_update_data = og_data.copy()
        old_update_data[u'sig'] = signature
        # ToDo: End
        log.info(u'Adding sig to update data')
        self._write_update_data(og_data, update_data, old_update_data)

    def _write_update_data(self, data, version, old_version):
        # Write version file to disk
        with open(self.version_data, u'w') as f:
            f.write(json.dumps(data, indent=2, sort_keys=True))
        log.info(u'Wrote version data to file system')

        with gzip.open(self.version_file, u'wb') as f:
            f.write(json.dumps(version, indent=2, sort_keys=True))
        log.info(u'Created version manifest in deploy dir')
        # ToDo: Remove in v1.0
        with open(self.old_version_file, u'w') as f:
            f.write(json.dumps(old_version, indent=2, sort_keys=True))
        log.info(u'Created old style version manifest in deploy dir')
        # ToDo: End

    def _load_update_data(self):
        # Loads version file into memory
        log.info(u"Loading version data")
        try:
            log.debug(u'Version data file path: {}'.format(self.version_data))
            with open(self.version_data, u'r') as f:
                update_data = json.loads(f.read())
            log.info(u'Version file loaded')
            return update_data
        except Exception as err:
            log.error(u'Version data file not found')
            log.debug(str(err), exc_info=True)
            log.info(u'Creating new version file')
            with open(self.version_data, u'w') as f:
                f.write(u'{}')
            log.info(u'Created new version file')
            return dict()
