import os
from random import choice
import sys

from nose import with_setup
from nose.tools import raises

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyi_updater.exceptions import FileCryptError
from pyi_updater.filecrypt import FileCrypt

PASSWORD = u'This is my password'
FILENAME = u'test.txt'
FILENAME_ENC = u'test.txt.enc'
RANDOM_DATA = u'This is some stuff that i want to test'.split(u' ')
FILE_DATA = []
LENGHTS = [8, 9, 10, 11]

for i in xrange(100):
    a = u' '.join(choice(RANDOM_DATA) for x in range(choice(LENGHTS)))
    FILE_DATA.append(a + u'\n')


def setup_func():
    with open(FILENAME, u'w') as f:
        for fd in FILE_DATA:
            f.write(fd)


def teardown_func():
    if os.path.exists(FILENAME):
        os.remove(FILENAME)
    if os.path.exists(FILENAME_ENC):
        os.remove(FILENAME_ENC)


@raises(FileCryptError)
def test_encrypt_no_filename():
    fc = FileCrypt()
    fc.encrypt()


@raises(FileCryptError)
def test_encrypt_no_file():
    fc = FileCrypt(FILENAME)
    fc.password = PASSWORD
    fc.encrypt()


@raises(FileCryptError)
def test_decrypt_no_filename():
    fc = FileCrypt()
    fc.decrypt()


@raises(FileCryptError)
def test_decrypt_no_file():
    fc = FileCrypt(FILENAME)
    fc.password = PASSWORD
    fc.decrypt()


# @with_setup(setup_func, teardown_func)
# def test_bad_change_password():
#     fc = FileCrypt(FILENAME)
#     fc.password = PASSWORD
#     fc.encrypt()
#     fc.password = None
#     assert fc.change_password('bad password', 'new password') is False


@with_setup(setup_func, teardown_func)
def test_change_password():
    fc = FileCrypt(FILENAME)
    fc.password = PASSWORD
    fc.encrypt()
    assert fc.change_password(PASSWORD, 'new password') is True


def test_update_password_timer():
    fc = FileCrypt()
    fc._update_timer()
    assert fc.password_timer != 0


def test_no_update_timer():
    fc = FileCrypt()
    fc._update_timer()
    test_time = fc.password_timer
    fc._update_timer()
    assert test_time == fc.password_timer


@with_setup(setup_func, teardown_func)
def test_file_enc_dec():
    fc = FileCrypt(FILENAME)
    fc.password = PASSWORD
    fc.encrypt()
    fc.password = PASSWORD
    fc.decrypt()
    with open(FILENAME, u'r') as f:
        og_data = f.readlines()

    assert og_data == FILE_DATA


@with_setup(setup_func, teardown_func)
def test_enc_file_name():
    fc = FileCrypt(FILENAME)
    fc.password = PASSWORD
    fc.encrypt()
    assert os.path.exists(FILENAME_ENC) is True


def test_plaintext_filename():
    test_filename = 'test.txt'
    fc = FileCrypt()
    set_filename, set_enc_filename = fc._set_filenames(test_filename)
    assert set_filename == FILENAME
    assert set_enc_filename == FILENAME_ENC


def test_ciphertext_filename():
    test_filename = 'test.txt.enc'
    fc = FileCrypt()
    filename, enc_filename = fc._set_filenames(test_filename)
    assert filename == u'test.txt'
    assert enc_filename == u'test.txt.enc'
