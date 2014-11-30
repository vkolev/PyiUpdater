from base64 import (urlsafe_b64encode as b_encode)
import getpass
import logging
import os
import time

from cryptography.fernet import Fernet
from pbkdf2 import pbkdf2_bin
from six.moves import input

from pyi_updater.exceptions import FileCryptError, FileCryptPasswordError


log = logging.getLogger(__name__)

SALT_VESION = '1'

SALT_VERSIONS = {
    '1': 1000,
    }


class FileCrypt(object):
    """Small wrapper around cryptography to make it easier to use
    with not-so-tuf.

    Args:
        filename (str): The name of the file to encrypt

        password_timeout (int): The number of seconds before
        needing to re-enter password. DEFAULT is 30.

        max_tries (int): The number of password attempts before
        program exists.  DEFAULT is 3
    """

    def __init__(self, filename=None, password_timeout=30, max_tries=3):
        self.data_dir = None
        self.salt_file = None
        self.password = None
        self.password_timer = 0
        self.password_max_tries = max_tries
        self.passwrod_timeout = password_timeout
        self.new_file(filename)

    def init_app(self, pyi):
        self.data_dir = pyi.config.get(u'DEV_DATA_DIR')
        if self.data_dir is not None:
            self.salt_file = os.path.join(self.data_dir, u'pyi-data',
                                          u'keys', u'salt')

    def new_file(self, filename=None):
        """Adds filename internally to be used for encryption and
        decryption. Also adds .enc to filename to be used  as
        encrypted filename.

        Args:

            filename (str): Path of file to be encrypted/decrypted
        """
        if filename is not None:
            self.filename, self.enc_filename = self._set_filenames(filename)
            log.debug(u'Filename: {}'.format(self.filename))
            log.debug(u'Enc Filename: {}'.format(self.enc_filename))
        else:
            self.filename = None
            self.enc_filename = None
            log.debug(u'No file to process yet.')

    def encrypt(self):
        """Will encrypt the file"""
        if self.filename is None:
            raise FileCryptError(u'Must set filename with new_file '
                                 'method call before you can encrypt',
                                 expected=True)

        if not os.path.exists(self.filename):
            raise FileCryptError(u'No file to encrypt.')

        with open(self.filename, u'r') as f:
            plain_data = f.read()
            log.debug(u'Got plain text')

        log.debug(u'Lets start this encryption process.')
        if self.password is None:
            self.password = self._get_password()
        fernet = Fernet(self.password)

        enc_data = fernet.encrypt(plain_data)

        with open(self.enc_filename, u'w') as f:
            f.write(enc_data)
            log.debug(u'Wrote encrypted '
                      'data to {}'.format(self.enc_filename))
        os.remove(self.filename)
        log.debug(u'Removed original file')
        self._del_internal_password()

    def decrypt(self, change_password=False):
        """Will decrypt the file"""
        if self.filename is None:
            raise FileCryptError(u'Must set filename with new_file '
                                 'method call before you can decrypt',
                                 expected=True)

        if not os.path.exists(self.enc_filename):
            log.error(u'No file to decrypt')
            raise FileCryptError(u'No file to decrypt')

        with open(self.enc_filename, u'r') as f:
            log.debug(u'Grabbing ciphertext.')
            enc_data = f.read()

        plain_data = None
        tries = 0
        while tries < self.password_max_tries:
            if self.password is None:
                self.password = self._get_password()
            log.debug(u'Tries = {}'.format(tries))
            fernet = Fernet(self.password)
            try:
                log.debug(u'Going to attempt to decrypt the file')

                plain_data = fernet.decrypt(enc_data)
                break
            except Exception as e:
                self.password = None
                input(u'\nInvalid Password.  Press enter to try again')
                log.debug(u'Invalid Password')
                log.error(str(e), exc_info=True)
                tries += 1

        if plain_data is not None:
            log.debug(u'Writing plaintext to file.')
            with open(self.filename, u'w') as f:
                f.write(plain_data)
            log.debug(u'Done writing to file.')
        else:
            if change_password is False:
                log.debug(u'To many fialed password attempts')
                raise FileCryptPasswordError(u'You entered to many wrong '
                                             'passwords.')
            else:
                raise FileCryptError('Wrong password')

    def change_password(self, old_pass, new_pass):
        """Will change password for encrypted file

        Args:
            old_pass (str): Old Password
            new_pass (str): New Password

        Returns:
            (bool) Meanings::

                True - Password change successful

                False - Password change failed
        """
        default_tries = self.password_max_tries
        self.password_max_tries = 1
        self.password = old_pass
        try:
            self.decrypt(change_password=True)
        except FileCryptError:
            self.password_max_tries = default_tries
            self.password = None
            return False

        self.password_max_tries = default_tries
        self.password = new_pass
        self.encrypt()
        return True

    def _set_filenames(self, filename):
        # Helper function to correctly set filename and
        # enc_filename instance attributes
        if filename.endswith(u'.enc'):
            filename_ = filename[:-4]
            enc_filename = filename
        else:
            filename_ = filename
            enc_filename = filename + u'.enc'
        return filename_, enc_filename

    def _get_password(self):
        # Gets user password without echoing to the console
        log.debug(u'Getting user password')
        temp_password = getpass.getpass(u'Enter password:\n-->')
        log.debug(u'Got you pass')
        self._update_timer()
        return self._gen_password(temp_password)

    def _gen_password(self, password, salt_info=None):
        if salt_info is None:
            salt_info = self._get_salt()
        iterations = SALT_VERSIONS[salt_info['version']]
        key = pbkdf2_bin(password, salt_info['salt'],
                         iterations=iterations, keylen=32)
        return b_encode(key)

    def _get_salt(self):
        for v in sorted(map(int, SALT_VERSIONS.keys()), reverse=True):
            v = str(v)
            salt_file = self.salt_file + u'.' + v
            if os.path.exists(salt_file):
                log.debug(u'Found salt file: {}'.format(salt_file))
                self.salt_file = salt_file
                with open(self.salt_file, u'r') as f:
                    salt = f.read()
                version = v
                break
        else:
            log.debug(u'Did not find salt file')
            salt = os.urandom(16)
            self.salt_file = self.salt_file + u'.' + SALT_VESION
            with open(self.salt_file, u'w') as f:
                f.write(salt)
            log.debug(u'Created salt file: {}'.format(self.salt_file))
            version = SALT_VESION
        return {u'salt': salt, 'version': version}

    def _update_timer(self):
        # Updates internal timer if not already past current time
        if self.password_timer < time.time():
            log.debug(u'Updating your internal timer.')
            self.password_timer = time.time() + float(self.passwrod_timeout)

    def _del_internal_password(self):
        # Deletes user password once its not needed.
        # i.e. when the file been encrypted or timer expired
        if self.password_timer < time.time():
            log.debug(u'About to delete internal password')
            self.password = None


if __name__ == '__main__':
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    s = logging.StreamHandler()
    s.setLevel(logging.DEBUG)
    log.addHandler(s)
