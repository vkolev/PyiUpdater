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
import bz2
from getpass import getpass
import gzip
import hashlib
import logging
import os
import re
import shutil
import StringIO
import subprocess
import sys
import tarfile
import time
import zipfile

from pyi_updater import settings
from pyi_updater.exceptions import UtilsError

log = logging.getLogger(__name__)

jms_utils = None
six = None


def check_repo():
    if not os.path.exists(settings.CONFIG_DATA_FOLDER):
        log.error('Not a PyiUpdater repo: must init first.')
        sys.exit(1)


def check_version(version):
    match = re.match(u'(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)',
                     version)
    if match is None:
        log.debug('Version did not match')
        return False
    else:
        log.debug('Version matched')
        return True


def convert_to_list(data, default=None):
    global six
    if six is None:
        six = lazy_import(u'six')
    if isinstance(data, list):
        return data
    if isinstance(data, tuple):
        return list(data)
    if isinstance(data, six.string_types):
        return [data]
    else:
        log.debug('Not of string of tuple')
        return default


def get_filename(name, version, platform, easy_data):
        """Gets full filename for given name & version combo

        Args:

           name (str): name of file to get full filename for

           version (str): version of file to get full filename for

           easy_data (dict): data file to search

        Returns:

           (str) Filename with extension
        """
        filename_key = u'{}*{}*{}*{}*{}'.format(u'updates', name, version,
                                                platform, u'filename')
        filename = easy_data.get(filename_key)

        log.debug(u"Filename for {}-{}: {}".format(name, version, filename))
        return filename


def get_hash(data):
    hash_ = hashlib.sha256(data).hexdigest()
    log.debug(u'Hash for binary data: {}'.format(hash_))
    return hash_


def get_highest_version(name, plat, easy_data):
    """Parses version file and returns the highest version number.

    Args:

       name (str): name of file to search for updates

       easy_data (dict): data file to search

    Returns:

       (str) Highest version number
    """
    version_key = u'{}*{}*{}'.format(u'latest', name, plat)
    version = easy_data.get(version_key)

    if version is not None:
        log.debug(u'Highest version: {}'.format(version))
    else:
        log.error(u'No updates for "{}" on {} exists'.format(name, plat))
    return version


def get_mac_dot_app_dir(directory):
    """Returns parent directory of mac .app

    Args:

       directory (str): Current directory

    Returns:

       (str): Parent directory of mac .app
    """
    return os.path.dirname(os.path.dirname(os.path.dirname(directory)))


def get_package_hashes(filename):
        log.debug(u'Getting package hashes')
        filename = os.path.abspath(filename)
        with open(filename, u'rb') as f:
            data = f.read()

        _hash = hashlib.sha256(data).hexdigest()
        log.debug(u'Hash for file {}: {}'.format(filename, _hash))
        return _hash


def get_version_number(package_name):
        # Parse package name and return version number
        # Extracts and returns version number from
        # given string
        re_str = u'(?P<version>[0-9]+\.[0-9]+\.[0-9]+)'
        try:
            v_n = re.compile(re_str).findall(package_name)[0]
            log.debug('Found version: {}'.format(v_n))
            return v_n
        except Exception as e:
            log.debug(str(e))
            raise UtilsError(u'Can not find version number', expected=True)


def gzip_decompress(data):
    compressed_file = StringIO.StringIO()
    compressed_file.write(data)
    #
    # Set the file's current position to the beginning
    # of the file so that gzip.GzipFile can read
    # its contents from the top.
    #
    compressed_file.seek(0)

    decompressed_file = gzip.GzipFile(fileobj=compressed_file, mode='rb')
    data = decompressed_file.read()
    compressed_file.close()
    decompressed_file.close()
    return data


def setup_appname(config):
    global jms_utils
    if jms_utils is None:
        jms_utils = lazy_import('jms_utils.terminal')
    if config.APP_NAME is not None:
        default = config.APP_NAME
    else:
        default = None
    config.APP_NAME = jms_utils.terminal.get_correct_answer(u'Please enter '
                                                            u'app name',
                                                            required=True,
                                                            default=default)


def setup_company(config):
    global jms_utils
    if jms_utils is None:
        jms_utils = lazy_import('jms_utils.terminal')
    if config.COMPANY_NAME is not None:
        default = config.COMPANY_NAME
    else:
        default = None
    temp = jms_utils.terminal.get_correct_answer(u'Please enter your comp'
                                                 u'any or name',
                                                 required=True,
                                                 default=default)
    config.COMPANY_NAME = temp


def setup_urls(config):
    global jms_utils
    if jms_utils is None:
        jms_utils = lazy_import('jms_utils.terminal')
    url = jms_utils.terminal.get_correct_answer(u'Enter a url to ping for '
                                                u'updates.', required=True)
    config.UPDATE_URLS = [url]
    while 1:
        answer = jms_utils.terminal.ask_yes_no(u'Would you like to add '
                                               u'another url for backup?',
                                               default='no')
        if answer is True:
            url = jms_utils.terminal.get_correct_answer(u'Enter another url.',
                                                        required=True)
            config.UPDATE_URLS.append(url)
        else:
            break


def setup_patches(config):
    global jms_utils
    if jms_utils is None:
        jms_utils = lazy_import('jms_utils.terminal')
    config.UPDATE_PATCHES = jms_utils.terminal.ask_yes_no(u'Would you like to '
                                                          u'enable patch upda'
                                                          u'tes?',
                                                          default=u'yes')


def setup_scp(config):
    global jms_utils
    if jms_utils is None:
        jms_utils = lazy_import('jms_utils.terminal')
    _temp = jms_utils.terminal.get_correct_answer(u'Enter remote dir',
                                                  required=True)
    config.REMOTE_DIR = _temp
    config.HOST = jms_utils.terminal.get_correct_answer(u'Enter host',
                                                        required=True)

    config.USERNAME = jms_utils.terminal.get_correct_answer(u'Enter '
                                                            u'usernmae',
                                                            required=True)


def setup_s3(config):
    global jms_utils
    if jms_utils is None:
        jms_utils = lazy_import('jms_utils.terminal')
    _temp = jms_utils.terminal.get_correct_answer(u'Enter access key ID',
                                                  required=True)
    config.USERNAME = _temp
    _temp = jms_utils.terminal.get_correct_answer(u'Enter bucket name',
                                                  required=True)
    config.REMOTE_DIR = _temp


def initial_setup(config):
    global jms_utils
    if jms_utils is None:
        jms_utils = lazy_import('jms_utils.terminal')
    setup_appname(config)
    setup_company(config)
    setup_urls(config)
    setup_patches(config)

    answer1 = jms_utils.terminal.ask_yes_no(u'Would you like to add scp '
                                            u'settings?', default='no')

    answer2 = jms_utils.terminal.ask_yes_no(u'Would you like to add S3 '
                                            'settings?', default='no')

    if answer1:
        setup_scp(config)

    if answer2:
        setup_s3(config)
    return config


def lazy_import(mod):
    return __import__(mod)


def make_archive(name, version, target):
    u"""Used to make archives of file or dir. Zip on windows and tar.gz
    on all other platforms

    Args:
        name - Name of app. Used to create final archive name

        version - Version of app. Used to create final archive name

        target - name of actual target file or dir.

    Returns:
         (str) - name of archive
    """
    jms_utils = lazy_import(u'jms_utils')
    file_dir = os.path.dirname(os.path.abspath(target))
    filename = u'{}-{}-{}'.format(name, jms_utils.system.get_system(), version)
    filename_path = os.path.join(file_dir, filename)

    print(u'starting archive')

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
    if jms_utils.system.get_system() == u'win':
        ext = u'.zip'
        with zipfile.ZipFile(filename_path + u'.zip', u'w') as zf:
            zf.write(target, temp_file)
    else:
        ext = u'.tar.gz'
        if os.path.isfile(target):
            with tarfile.open(filename_path + u'.tar.gz', u'w:gz') as tar:
                tar.add(target, temp_file)
        else:
            shutil.make_archive(filename, u'gztar', file_dir, temp_file)

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


def parse_platform(name):
        try:
            platform_name = re.compile(u'[macnixwr64]{3,5}').findall(name)[0]
            log.debug(u'Platform name is: {}'.format(platform_name))
        except IndexError:
            raise UtilsError('')

        return platform_name


def pretty_time(sec):
    return time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime(sec))


def remove_dot_files(files):
        # Removes hidden files from file list
        new_list = []
        for l in files:
            if not l.startswith(u'.'):
                new_list.append(l)
        return new_list


def run(cmd):
    log.debug(u'Command: {}'.format(cmd))
    exit_code = subprocess.call(cmd)
    return exit_code


def verify_password(message):
    six = lazy_import(u'six')
    while 1:
        password1 = getpass(u'{}: '.format(message))
        password2 = getpass(u'{} again: '.format(message))
        if password1 == password2:
            return password1
        else:
            six.moves.input(u'\n\nPasswords do not match. '
                            u'Press Enter to try again.')


def vstr_2_vtuple(x):
    return tuple(map(int, x.split('.')))


def vtuple_2_vstr(x):
    return '.'.join(map(str, x))


class bsdiff4_py(object):
    u"""Pure-python version of bsdiff4 module that can only patch, not diff.

    By providing a pure-python fallback, we don't force frozen apps to
    bundle the bsdiff module in order to make use of patches.  Besides,
    the patch-applying algorithm is very simple.
    """
    @staticmethod
    def patch(source, patch):
        six = lazy_import(u'six')
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
        source = six.BytesIO(source)
        result = six.BytesIO()
        bdiff = six.BytesIO(bdiff)
        bextra = six.BytesIO(bextra)
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


class EasyAccessDict(object):

    def __init__(self, dict_=None, sep=u'*'):
        self.load(dict_, sep)

    def load(self, dict_, sep=u'*'):
        self.sep = sep
        if not isinstance(dict_, dict):
            log.debug(u'Did not pass dict')
            self.dict = dict()
            log.debug(u'Loading empty dict')
        else:
            self.dict = dict_

    def get(self, key):
        try:
            layers = key.split(self.sep)
            value = self.dict
            for key in layers:
                value = value[key]
            log.debug(u'Found Key')
            return value
        except KeyError:
            log.debug(u'Key Not Found')
            return None
        except Exception as err:
            log.error(str(err), exc_info=True)
            return None

    # Because I always for get call the get method
    def __call__(self, key):
        return self.get(key)

    def __str__(self):
        return str(self.dict)


class Version(object):

    def __init__(self, version):
        self.version_str = version
        self.version_tuple = self.convert_2_tuple(self.version_str)
        self.major = self.version_tuple[0]
        try:
            self.minor = self.version_tuple[1]
        except IndexError:
            self.minor = 0
        try:
            self.patch = self.version_tuple[2]
        except IndexError:
            self.patch = 0

    def convert_2_tuple(self, version):
        return tuple(map(int, version.split(u'.')))

    def __str__(self):
        return self.version_str

    def __eq__(self, obj):
        if hasattr(obj, 'version_tuple') is False:
            return False
        return self.version_tuple == obj.version_tuple

    def __ne__(self, obj):
        if hasattr(obj, 'version_tuple') is False:
            return False
        return self.version_tuple != obj.version_tuple

    def __lt__(self, obj):
        if hasattr(obj, 'version_tuple') is False:
            return False
        return self.version_tuple < obj.version_tuple

    def __gt__(self, obj):
        if hasattr(obj, 'version_tuple') is False:
            return False
        return self.version_tuple > obj.version_tuple

    def __le__(self, obj):
        if hasattr(obj, 'version_tuple') is False:
            return False
        return self.version_tuple <= obj.version_tuple

    def __ge__(self, obj):
        if hasattr(obj, 'version_tuple') is False:
            return False
        return self.version_tuple >= obj.version_tuple


def _decode_offt(bytes):
    u"""Decode an off_t value from a string.

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
