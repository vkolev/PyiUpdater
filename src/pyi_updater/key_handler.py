from __future__ import print_function
import json
import logging
import os
import shutil
import sys

import ed25519
from jms_utils.paths import ChDir
import six

from pyi_updater.exceptions import FileCryptPasswordError, KeyHandlerError
from pyi_updater.filecrypt import FileCrypt

if six.PY3 is True:
    long = int

log = logging.getLogger(__name__)


class KeyHandler(object):
    """KeyHanlder object is used to manage keys used for signing updates

    Kwargs:
        app (obj): Config object to get config values from
    """

    def __init__(self, app=None):
        self.fc = None
        if app:
            self.init_app(app)

    def init_app(self, obj):
        """Sets up client with config values from obj

        Args:
            obj (instance): config object
        """
        # Copies and sets all needed config attributes
        # for this object
        self.app_name = obj.config.get(u'APP_NAME')
        self.data_dir = obj.config.get(u'DEV_DATA_DIR',)
        if self.data_dir is not None:
            self.data_dir = os.path.join(self.data_dir, u'pyi-data')
            self.keys_dir = os.path.join(self.data_dir, u'keys')
            self.deploy_dir = os.path.join(self.data_dir, u'deploy')
            self.version_file = os.path.join(self.data_dir, u'version.json')
            if not os.path.exists(self.keys_dir):
                log.debug(u'Creating keys directory')
                # Just in case folders got deleted before we start work :)
                os.makedirs(self.keys_dir)
        else:
            log.error(u'Dev_DATA_DIR is None. Setup Failed')

        # Private key setup
        self.private_key_name = self.app_name + u'.pem'

        # Public key setup
        self.public_key_name = self.app_name + u'.pub'

        self.key_encoding = 'base64'

        # Set to true when running tests
        self.test = False

    def make_keys(self, overwrite=False):
        """Makes public and private keys for signing and verification

        Kwargs:
            overwrite (bool): Determines if existing keys are overwritten
        """
        # Makes a set of private and public keys
        # Used for authentication
        log.debug(u'Making keys')

        self.privkey, self.pubkey = ed25519.create_keypair()
        self._write_keys_to_file(overwrite)

    def sign_update(self):
        """Signs version file with private key

        Proxy method for :meth:`_load_private_key`, :meth:`_add_sig` &
        :meth:`_write_update_data`
        """
        # Loads private key
        # Loads version file to memory
        # Signs Version file
        # Writes version file back to disk
        self._load_private_key()
        self._add_sig()
        self._write_update_data()

    def get_public_key(self):
        """Returns (object): Public Key
        """
        public_key_path = os.path.join(self.keys_dir, self.public_key_name)
        log.debug(u'Public key path: {}'.format(public_key_path))
        if not os.path.exists(public_key_path):
            raise KeyHandlerError(u'You do not have a public key',
                                  expected=True)
        public_key_path = os.path.join(self.keys_dir, self.public_key_name)
        with open(public_key_path, u'r') as f:
            pub_key_data = f.read()
        return pub_key_data

    def copy_decrypted_private_key(self):
        """Copies decrypted private key."""
        privkey = os.path.join(self.keys_dir, self.private_key_name)
        log.debug(u'Private Key Path: {}'.format(privkey))
        self.fc.new_file(privkey)
        try:
            self.fc.decrypt()
        except FileCryptPasswordError:
            sys.exit(u'Too many failed password')
        shutil.copy(privkey, privkey + u' copy')
        self.fc.encrypt()

    def print_public_key(self):
        """Prints public key data to console"""
        public = os.path.join(self.keys_dir, self.public_key_name)
        if os.path.exists(public):
            with open(public, u'r') as f:
                key = f.read()
            print(u'Public Key:\n{}\n\n'.format(key))
        else:
            print(u'No Public Key Found')

    def _load_private_key(self):
        # Loads private key
        log.debug(u'Loading private key')
        priv_key_path = os.path.join(self.keys_dir, self.private_key_name)
        log.debug(u'private key path: {}'.format(priv_key_path))
        if not os.path.exists(priv_key_path):
            if not not os.path.exists(priv_key_path + u'.enc'):
                raise KeyHandlerError(u"You don't have any keys",
                                      expected=True)
        privkey = os.path.join(self.keys_dir, self.private_key_name)

        # If we are testing we can skip the decrypt set since nose
        # cannot provide passwords.
        if self.test:
            with open(privkey, u'r') as pk:
                self.privkey = ed25519.SigningKey(pk.read(),
                                                  encoding='base64')
            return

        self.fc.new_file(privkey)
        try:
            self.fc.decrypt()
        except FileCryptPasswordError:
            sys.exit(u'Too many failed password attempts')
        except:
            log.debug(u'Nothing to decrypt')

        if os.path.exists(privkey):
            try:
                with open(privkey, u'r') as pk:
                    key_data = pk.read()
                self.privkey = ed25519.SigningKey(key_data,
                                                  encoding=self.key_encoding)
            except Exception as e:
                log.error(e, exc_info=True)
                raise KeyHandlerError(u'Invalid private key')
        else:
            raise KeyHandlerError(u'Private key not found')

        self.fc.encrypt()

    def _add_sig(self):
        # Adding new signature to version file
        log.debug(u'Adding signature to version file...')
        if not self.privkey:
            log.debug(u'Private key not loaded')
            raise KeyHandlerError(u'You must load your privkey first',
                                  expected=True)

        update_data = self._load_update_data()
        if u'sig' in update_data:
            log.debug(u'Deleting sig')
            del update_data[u'sig']
        _data = json.dumps(update_data, sort_keys=True)
        signature = self.privkey.sign(six.b(_data),
                                      encoding=self.key_encoding)

        # Finish conversion here
        update_data = json.loads(_data)
        update_data[u'sig'] = signature
        log.debug(u'Adding sig to update data')
        self.update_data = update_data

    def _write_update_data(self):
        # Write version file "with new sig" to disk
        log.debug(u'Wrote version data')
        if self.update_data:
            with open(self.version_file, u'w') as f:
                f.write(json.dumps(self.update_data, indent=2,
                        sort_keys=True))
            with ChDir(self.data_dir):
                shutil.copy(u'version.json', self.deploy_dir)
        else:
            msg = u'You must sign update data first'
            raise KeyHandlerError(msg, expected=True)

    def _write_keys_to_file(self, overwrite=False):
        # Writes keys to disk
        #
        # Args:
        #    overwrite (bool): Determines if existing keys are overwritten

        # Writes the public and private keys to files
        public = os.path.join(self.keys_dir, self.public_key_name)
        private = os.path.join(self.keys_dir, self.private_key_name)
        if os.path.exists(public) and os.path.exists(private):
            if overwrite is False:
                log.debug(u'Cannot overwrite old key files.')
                log.debug(u'Pass overwrite=True to make_keys to overwrite')
                return
            else:
                log.debug(u'About to overwrite old keys')
        log.debug(u'Writing keys to file')
        with open(private, u'w') as f:
            f.write(self.privkey.to_ascii(encoding=self.key_encoding))

        # If we are not testing, encrypt the file
        # Only the private key.
        if self.test is False:
            self.fc.new_file(private)
            self.fc.encrypt()
        with open(public, u'w') as f:
            f.write(self.pubkey.to_ascii(encoding=self.key_encoding))

    def _load_update_data(self):
        # Loads version file into memory
        log.debug(u"Loading version file")
        try:
            log.debug(u'Version file path: {}'.format(self.version_file))
            with open(self.version_file, 'r') as f:
                update_data = json.loads(f.read())
            log.debug(u'Version file loaded')
            return update_data
        except Exception as e:
            log.error(e)
            raise KeyHandlerError(u'Version file not found',
                                  expected=True)

    def _add_filecrypt(self, fc=None):
        # Using a single file crypt object module wide.
        # Helps with password timeout
        if fc is None:
            self.fc = FileCrypt()
        else:
            self.fc = fc
