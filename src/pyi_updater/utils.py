from getpass import getpass
import hashlib
import logging
import os
import re
import struct
import sys

from six.moves import input

from pyi_updater.exceptions import UtilsError

log = logging.getLogger(__name__)
FROZEN = getattr(sys, u'frozen', False)


if FROZEN:  # pragma: no cover
    # we are running in a |PyInstaller| bundle
    cwd_ = os.path.dirname(sys.argv[0])
else:
    # we are running in a normal Python environment
    cwd_ = os.getcwd()


class StarAccessDict(object):

    def __init__(self, dict_=None):
        self.load(dict_)

    def load(self, dict_):
        if not isinstance(dict_, dict):
            self.dict = dict()
        else:
            self.dict = dict_

    def get(self, key):
        try:
            layers = key.split('*')
            value = self.dict
            for key in layers:
                value = value[key]
                print value
            log.debug('Found Key')
            return value
        except KeyError:
            log.debug('Key Not Found')
            return None
        except Exception as err:
            log.error(str(err), exc_info=True)
            return None


def verify_password(message):
    while 1:
        password1 = getpass('{}: '.format(message))
        password2 = getpass('{} again: '.format(message))
        if password1 == password2:
            return password1
        else:
            input('\n\nPasswords do not match. Press Enter to try again.')


def get_hash(data):
    hash_ = hashlib.sha256(data).hexdigest()
    log.debug(u'Hash for binary data: {}'.format(hash_))
    return hash_


def remove_dot_files(files):
        # Removes hidden files from file list
        new_list = []
        for l in files:
            if not l.startswith(u'.'):
                new_list.append(l)
        return new_list


def get_version_number(package_name):
        # Parse package name and return version number
        # Extracts and returns version number from
        # given string
        try:
            v_n = \
                re.compile(u'[0-9]+\.[0-9]+\.[0-9]+').findall(package_name)[0]
            return v_n
        except Exception as e:
            log.debug(str(e))
            raise UtilsError('Can not find version number', expected=True)


def version_string_to_tuple(version):
        return tuple(map(int, version.split('.')))


def version_tuple_to_string(version):
    return '.'.join(map(str, version))


# Big Thanks to FiloSottile for making this lib for us
# All Files can be found in this gist
# https://gist.github.com/FiloSottile/4340076
def rsa_verify(message, signature, key):
    def b(x):
        if sys.version_info[0] == 2:
            return x
        else:
            return x.encode('latin1')
    assert(type(message) == type(b('')))
    block_size = 0
    n = key[0]
    while n:
        block_size += 1
        n >>= 8
    signature = pow(int(signature, 16), key[1], key[0])
    raw_bytes = []
    while signature:
        raw_bytes.insert(0, struct.pack("B", signature & 0xFF))
        signature >>= 8
    signature = (block_size - len
                 (raw_bytes)) * b('\x00') + b('').join(raw_bytes)
    if signature[0:2] != b('\x00\x01'):
        return False
    signature = signature[2:]
    if not b('\x00') in signature:
        return False
    signature = signature[signature.index(b('\x00'))+1:]
    if not signature.startswith(b('\x30\x31\x30\x0D\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x01\x05\x00\x04\x20')):
        return False
    signature = signature[19:]
    if signature != hashlib.sha256(message).digest():
        return False
    return True


def get_package_hashes(filename):
        log.debug(u'Getting package hashes')
        filename = os.path.abspath(filename)
        with open(filename, u'rb') as f:
            data = f.read()

        _hash = hashlib.sha256(data).hexdigest()
        log.debug(u'Hash for file {}: {}'.format(filename, _hash))
        return _hash


def parse_platform(name):
        try:
            platform_name = re.compile(u'[macnixwr64]{3,5}').findall(name)[0]
            log.debug(u'Platform name is: {}'.format(platform_name))
        except IndexError:
            raise UtilsError('')

        return platform_name
