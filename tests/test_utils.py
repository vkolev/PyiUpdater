import os
import sys

from jms_utils import FROZEN
from jms_utils.paths import cwd
from nose import with_setup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli.ui.menu_utils import ask_yes_no

from pyi_updater.utils import (get_hash,
                               get_package_hashes,
                               version_string_to_tuple,
                               version_tuple_to_string
                               )

home_dir = os.path.expanduser('~')


def test_frozen():
    assert FROZEN is False


def test_cwd():
    assert cwd == os.getcwd()


def test_ask_yes_no_true():
    yes = ask_yes_no('Test True', answer='yes')
    assert yes is True


def test_ask_yes_no_false():
    no = ask_yes_no('Test False', answer='no')
    assert no is False


def setup_hash():
    with open('hash-test.txt', 'w') as f:
        f.write('I should find some lorem text' * 123)


def teardown_hash():
    if os.path.exists('hash-test.txt'):
        os.remove('hash-test.txt')


@with_setup(setup_hash, teardown_hash)
def test_package_hash():
    digest = 'cb44ec613a594f3b20e46b768c5ee780e0a9b66ac6d5ac1468ca4d3635c4aa9b'
    assert digest == get_package_hashes('hash-test.txt')


def test_get_hash():
    digest = '380fd2bf3d78bb411e4c1801ce3ce7804bf5a22d79405d950e5d5c8f3169fca0'
    assert digest == get_hash('Get this hash please')


def test_string_to_tuple():
    assert (1, 2, 3) == version_string_to_tuple('1.2.3')


def test_tuple_to_stirng():
    assert '1.2.3' == version_tuple_to_string((1, 2, 3))
