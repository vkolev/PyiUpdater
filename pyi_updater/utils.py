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


from pyi_updater.exceptions import UtilsError

log = logging.getLogger(__name__)


class EasyAccessDict(object):

    def __init__(self, dict_=None, sep=u'*'):
        self.load(dict_, sep)

    # Because I always for get call the get method
    def __call__(self, key):
        return self.get(key)

    def load(self, dict_, sep=u'*'):
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
            log.debug(u'Found Key')
            return value
        except KeyError:
            log.debug(u'Key Not Found')
            return None
        except Exception as err:
            log.error(str(err), exc_info=True)
            return None


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
            raise UtilsError(u'Can not find version number', expected=True)


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


def ask_yes_no(question, default='no', answer=None):
    u"""Will ask a question and keeps prompting until
    answered.

    Args:
        question (str): Question to ask end user

    Kwargs:
        default (str): Default answer if user just press enter at prompt

    Returns:
        bool. Meaning::

            True - Answer is  yes

            False - Answer is no
    """
    six = lazy_import(u'six')
    default = default.lower()
    yes = [u'yes', u'ye', u'y']
    no = [u'no', u'n']
    if default in no:
        help_ = u'[N/y]?'
        default = False
    else:
        default = True
        help_ = u'[Y/n]?'
    while 1:
        display = question + '\n' + help_
        if answer is None:
            log.debug(u'Under None')
            answer = six.moves.input(display)
            answer = answer.lower()
        if answer == u'':
            log.debug(u'Under blank')
            return default
        if answer in yes:
            log.debug(u'Must be true')
            return True
        elif answer in no:
            log.debug(u'Must be false')
            return False
        else:
            sys.stdout.write(u'Please answer yes or no only!\n\n')
            sys.stdout.flush()
            answer = None
            six.moves.input(u'Press enter to continue')
            sys.stdout.write('\n\n\n\n\n')
            sys.stdout.flush()


def get_correct_answer(question, default=None, required=False,
                       answer=None, is_answer_correct=None):
    six = lazy_import(u'six')
    while 1:
        if default is None:
            msg = u' - No Default Available'
        else:
            msg = (u'\n[DEFAULT] -> {}\nPress Enter To '
                   u'Use Default'.format(default))
        prompt = question + msg + u'\n--> '
        if answer is None:
            answer = six.moves.input(prompt)
        if answer == '' and required and default is not None:
            print(u'You have to enter a value\n\n')
            six.moves.input(u'Press enter to continue')
            print(u'\n\n')
            answer = None
            continue
        if answer == u'' and default is not None:
            answer = default
        _ans = ask_yes_no(u'You entered {}, is this '
                          u'correct?'.format(answer),
                          answer=is_answer_correct)
        if _ans:
            return answer
        else:
            answer = None


def initial_setup(config):
    config.APP_NAME = get_correct_answer(u'Please enter app name',
                                         required=True)

    config.COMPANY_NAME = get_correct_answer(u'Please enter your '
                                             u'company or name', required=True)

    config.DEV_DATA_DIR = os.getcwd()

    url = get_correct_answer(u'Enter a url to ping for updates.',
                             required=True)
    config.UPDATE_URLS = [url]
    while 1:
        answer = ask_yes_no(u'Would you like to add another '
                            u'url for backup?', default='no')
        if answer is True:
            url = get_correct_answer(u'Enter another url.',
                                     required=True)
            config.UPDATE_URLS.append(url)
        else:
            break

    config.UPDATE_PATCHES = ask_yes_no(u'Would you like to enable patch '
                                       u'updates?', default=u'yes')

    answer1 = ask_yes_no(u'Would you like to add scp settings?',
                         default='no')

    answer2 = ask_yes_no(u'Would you like to add S3 settings?',
                         default='no')

    if answer1:
        config.REMOTE_DIR = get_correct_answer(u'Enter remote dir',
                                               required=True)
        config.HOST = get_correct_answer(u'Enter host', required=True)

        config.USERNAME = get_correct_answer(u'Enter usernmae',
                                             required=True)

    if answer2:
        config.USERNAME = get_correct_answer(u'Enter access key ID',
                                             required=True)
        config.REMOTE_DIR = get_correct_answer(u'Enter bucket name',
                                               required=True)
    return config


# Makes inputting directory more like shell
def directory_fixer(_dir):
    if _dir.startswith(u'~'):
        log.debug(u'Expanding ~ to full user path')
        _dir = _dir[2:]
        _dir = os.path.join(os.path.expanduser(u'~'), _dir)
    return _dir


def count_contents(d):
    jms_utils = lazy_import(u'jms_utils')
    with jms_utils.paths.ChDir(d):
        count = len(os.listdir(os.getcwd()))
    return count


def lazy_import(mod):
    return __import__(mod)
