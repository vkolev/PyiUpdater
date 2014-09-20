from nose import with_setup
import os
from random import choice
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyi_updater import FileCrypt

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
