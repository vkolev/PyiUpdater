from __future__ import print_function
import bz2
from getpass import getpass
import hashlib
import logging
import os
import re
import shutil
import sys
import tarfile
import zipfile

from jms_utils.system import get_system
from six import BytesIO
from six.moves import input

from pyi_updater.exceptions import UtilsError

log = logging.getLogger(__name__)


class EasyAccessDict(object):

    def __init__(self, dict_=None, sep='*'):
        self.load(dict_, sep)

    # Because I always for get call the get method
    def __call__(self, key):
        return self.get(key)

    def load(self, dict_, sep='*'):
        self.sep = sep
        if not isinstance(dict_, dict):
            self.dict = dict()
        else:
            self.dict = dict_

    def get(self, key):
        try:
            layers = key.split(self.sep)
            value = self.dict
            for key in layers:
                value = value[key]
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


def vstr_2_vtuple(x):
    return tuple(map(int, x.split('.')))


def vtuple_2_vstr(x):
    return '.'.join(map(str, x))


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


class bsdiff4_py(object):
    """Pure-python version of bsdiff4 module that can only patch, not diff.

    By providing a pure-python fallback, we don't force frozen apps to
    bundle the bsdiff module in order to make use of patches.  Besides,
    the patch-applying algorithm is very simple.
    """
    @staticmethod
    def patch(source, patch):
        #  Read the length headers
        l_bcontrol = _decode_offt(patch[8:16])
        l_bdiff = _decode_offt(patch[16:24])
        l_target = _decode_offt(patch[24:32])
        #  Read the three data blocks
        e_bcontrol = 32 + l_bcontrol
        e_bdiff = e_bcontrol + l_bdiff
        bcontrol = bz2.decompress(patch[32:e_bcontrol])
        bdiff = bz2.decompress(patch[e_bcontrol:e_bdiff])
        bextra = bz2.decompress(patch[e_bdiff:])
        #  Decode the control tuples
        tcontrol = []
        for i in xrange(0, len(bcontrol), 24):
            tcontrol.append((
                _decode_offt(bcontrol[i:i+8]),
                _decode_offt(bcontrol[i+8:i+16]),
                _decode_offt(bcontrol[i+16:i+24]),
            ))
        #  Actually do the patching.
        #  This is the bdiff4 patch algorithm in slow, pure python.
        source = BytesIO(source)
        result = BytesIO()
        bdiff = BytesIO(bdiff)
        bextra = BytesIO(bextra)
        for (x, y, z) in tcontrol:
            diff_data = bdiff.read(x)
            orig_data = source.read(x)
            if sys.version_info[0] < 3:
                for i in xrange(len(diff_data)):
                    result.write(chr((ord(diff_data[i]) +
                                 ord(orig_data[i])) % 256))
            else:
                for i in xrange(len(diff_data)):
                    result.write(bytes([(diff_data[i] + orig_data[i]) % 256]))
            result.write(bextra.read(y))
            source.seek(z, os.SEEK_CUR)
        return result.getvalue()


def _decode_offt(bytes):
    """Decode an off_t value from a string.

    This decodes a signed integer into 8 bytes.  I'd prefer some sort of
    signed vint representation, but this is the format used by bsdiff4.
    """
    if sys.version_info[0] < 3:
        bytes = map(ord, bytes)
    x = bytes[7] & 0x7F
    for b in xrange(6, -1, -1):
        x = x * 256 + bytes[b]
    if bytes[7] & 0x80:
        x = -x
    return x


def make_archive(name, version, target):
    """Used to make archives of file or dir. Zip on windows and tar.gz
    on all other platforms

    Args:
        name - Name of app. Used to create final archive name

        version - Version of app. Used to create final archive name

        target - name of actual target file or dir.

    Returns:
         (str) - name of archive
    """
    file_dir = os.path.dirname(os.path.abspath(target))
    filename = '{}-{}-{}'.format(name, get_system(), version)
    filename_path = os.path.join(file_dir, filename)

    print('starting archive')

    ext = os.path.splitext(target)[1]
    temp_file = name + ext

    # Remove file if it exists. Found during testing...
    if os.path.exists(temp_file):
        if os.path.isdir(temp_file):
            shutil.rmtree(temp_file, ignore_errors=True)
        else:
            os.remove(temp_file)
    if os.path.isfile(target):
        shutil.copy(target, temp_file)
    else:
        shutil.copytree(target, temp_file)
    # Only use zip on windows. Zip doens't preserve file
    # permissions on nix & mac
    if get_system() == u'win':
        ext = u'.zip'
        with zipfile.ZipFile(filename_path + '.zip', 'w') as zf:
            zf.write(target, temp_file)
    else:
        ext = u'.tar.gz'
        if os.path.isfile(target):
            with tarfile.open(filename_path + '.tar.gz', 'w:gz') as tar:
                tar.add(target, temp_file)
        else:
            shutil.make_archive(filename, 'gztar', file_dir, temp_file)

    if os.path.isfile(temp_file):
        os.remove(temp_file)
    else:
        shutil.rmtree(temp_file, ignore_errors=True)

    # if keep is False:
        # if os.path.isfile(target):
            # os.remove(target)
        # else:
            # shutil.rmtree(target, ignore_errors=True)

    return filename + ext
