from __future__ import print_function
from binascii import hexlify
import json
import logging
import os
import shutil
import sys

from Crypto.PublicKey import RSA
import Crypto.Signature.PKCS1_v1_5
import Crypto.Hash.SHA256
from six import PY3

from pyi_updater.exceptions import FileCryptPasswordError, KeyHandlerError
from pyi_updater.filecrypt import FileCrypt

if Crypto is None:  # pragma: no cover
    KeyHandlerError(u'You must have PyCrypto installed.',
                    expected=True)
if PY3 is True:
    long = int

log = logging.getLogger(__name__)


class KeyHandler(object):
    """KeyHanlder object is used to manage keys used for signing updates

    Kwargs:
        app (obj): Config object to get config values from
    """

    def __init__(self, app=None):
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
        self.data_dir = obj.config.get(u'DEV_DATA_DIR')
        if self.data_dir is not None:
            self.data_dir = os.path.join(self.data_dir, u'pyi-data')
            self.keys_dir = os.path.join(self.data_dir, u'keys')
            self.version_file = os.path.join(self.data_dir, u'version.json')
            if not os.path.exists(self.keys_dir):
                log.debug(u'Creating keys directory')
                # Just in case folders got deleted before we start work :)
                os.makedirs(self.keys_dir)
        else:
            log.error(u'Dev_DATA_DIR is None. Setup Failed')

        # Private key setup
        self.private_key_name = obj.config.get(u'PRIVATE_KEY_NAME')
        if self.private_key_name is None:
            # Using the app name for key name if not provided
            self.private_key_name = self.app_name + u'.pem'
        if not self.private_key_name.endswith(u'.pem'):
            # Adding extension if not already provided.
            self.private_key_name += u'.pem'

        # Public key setup
        self.public_key_name = obj.config.get(u'PUBLIC_KEY_NAME')
        if self.public_key_name is None:
            # Using app name for key name if not provided
            self.public_key_name = self.app_name + u'.pub'
        if not self.public_key_name.endswith(u'.pub'):
            # Adding extension if not already provided.
            self.public_key_name += u'.pub'

        self.key_length = obj.config.get(u'KEY_LENGTH', 2048)
        # Have to perform this check in case user passed None
        # to KEY_LENGTH in config file
        if self.key_length is None:
            self.key_length = 2048

        # FileCrypt object
        self.fc = None
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
        rsa_key_object = RSA.generate(int(self.key_length))
        # This is the private key, keep this secret. You'll need
        # it to sign new updates.

        self.privkey = rsa_key_object.exportKey(format=u'PEM')

        public_key_object = rsa_key_object.publickey()
        # This is the public key you must distribute with your
        # program and pass to rsa_verify.
        self.pubkey = (public_key_object.n, public_key_object.e)
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
        if not self._find_public_key():
            raise KeyHandlerError(u'You do not have a public key',
                                  expected=True)
        public_key_path = os.path.join(self.keys_dir, self.public_key_name)
        with open(public_key_path, u'r') as f:
            pub_key_data = f.read()
        return KeyHandler._pub_key_string_to_tuple(pub_key_data)

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

    def print_keys_to_console(self):
        """Prints public key and private key data to console"""
        self._load_private_key()
        print(u'Private Key:\n{}\n\n'.format(self.privkey))
        self.print_public_key()

    def print_public_key(self):
        """Prints public key data to console"""
        public = os.path.join(self.keys_dir, self.public_key_name)
        if os.path.exists(public):
            with open(public, u'r') as f:
                key = f.read()
            print(u'Public Key:\n{}\n\n'.format(key))
        else:
            print(u'No Public Key Found')

    def print_key_names_to_console(self):
        """Prints name of public and private key to console"""
        print(u'Private Key:\n{}\n\n'.format(self.private_key_name))
        print(u'Public Key:\n{}\n\n'.format(self.public_key_name))

    def _load_private_key(self):
        # Loads private key
        log.debug(u'Loading private key')
        if not self._find_private_key():
            raise KeyHandlerError(u"You don't have any keys",
                                  expected=True)
        privkey = os.path.join(self.keys_dir, self.private_key_name)

        # If we are testing we can skip the decrypt set since nose
        # cannot provide passwords.
        if self.test:
            with open(privkey, u'r') as pk:
                self.privkey = RSA.importKey(pk.read())
            return

        self.fc.new_file(privkey)
        if self.test is False:
            try:
                self.fc.decrypt()
            except:
                log.warning(u'Nothing to decrypt')

        if os.path.exists(privkey):
            try:
                with open(privkey, u'r') as pk:
                    self.privkey = RSA.importKey(pk.read())
            except Exception as e:
                log.error(e, exc_info=True)
                raise KeyHandlerError(u'Invalid private key')
        else:
            raise KeyHandlerError(u'Private key not found')

        if self.test is False:
            self.fc.encrypt()

    def _add_sig(self):
        # Adding new signature to version file
        log.debug(u'Adding signature to version file...')
        if not self.privkey:
            log.warning(u'Private key not loaded')
            raise KeyHandlerError(u'You must load your privkey first',
                                  expected=True)

        update_data = self._load_update_data()
        if u'sig' in update_data:
            log.debug(u'Deleting sig')
            del update_data[u'sig']
        _data = json.dumps(update_data, sort_keys=True)
        _data_hash = Crypto.Hash.SHA256.new(_data)
        signer = Crypto.Signature.PKCS1_v1_5.new(self.privkey)
        signature = signer.sign(_data_hash)

        update_data = json.loads(_data)
        update_data[u'sig'] = hexlify(signature)
        log.debug(u'Adding sig to update data')
        self.update_data = update_data

    def _write_update_data(self):
        # Write version file "with new sig" to disk
        log.debug(u'Wrote version data')
        if self.update_data:
            with open(self.version_file, u'w') as f:
                f.write(json.dumps(self.update_data, indent=2,
                        sort_keys=True))
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
                log.warning(u'About to overwrite old keys')
        log.debug(u'Writing keys to file')
        with open(private, u'w') as pri:
            pri.write(self.privkey)
        if self.test is False:
            self.fc.new_file(private)
            self.fc.encrypt()
        with open(public, u'w') as pub:
            pub.write(str(self.pubkey))

    def _find_private_key(self):
        # Searches keys folder for private key to sign version file
        priv_key_path = os.path.join(self.keys_dir, self.private_key_name)
        log.debug(u'private key path: {}'.format(priv_key_path))
        if os.path.exists(priv_key_path + u'.enc') or \
                os.path.exists(priv_key_path):
            log.debug(u'Found private key')
            return True
        log.debug(u"Didn't find private key")
        return False

    def _find_public_key(self):
        # Searches keys folder for public key
        public_key_path = os.path.join(self.keys_dir, self.public_key_name)
        log.debug(u'Private key path: {}'.format(public_key_path))
        if os.path.exists(public_key_path):
            log.debug(u'Found public key')
            return True
        log.debug(u"Didn't find public key")
        return False

    @staticmethod
    def _pub_key_string_to_tuple(x):
        x = x.replace(u'(', u'')
        x = x.replace(u')', u'')
        x = x.split(u',')
        return (long(x[0]), long(x[1]))

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
