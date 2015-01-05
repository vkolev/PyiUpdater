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


import os

from jms_utils import FROZEN
from jms_utils.system import get_system
from nose import with_setup

from pyi_updater.utils import (get_hash,
                               get_package_hashes,
                               make_archive,
                               vstr_2_vtuple,
                               vtuple_2_vstr
                               )

home_dir = os.path.expanduser('~')

FILENAME = U'{}-archive'.format(get_system())


def setup_archive():
    with open(FILENAME, u'w') as f:
        msg = 'This is the life\n\n'
        for i in range(50):
            f.write(msg)


def teardown_archive():
    arch = get_system()
    name = u'done-{}-0.1.1.tar.gz'.format(arch)
    if os.path.exists(name):
        os.remove(name)
    if os.path.exists(FILENAME):
        os.remove(FILENAME)


@with_setup(setup_archive, teardown_archive)
def test_make_archive():
    arch = get_system()
    good_name = u'done-{}-0.1.1.tar.gz'.format(arch)
    print good_name
    name = make_archive(u'done', u'0.1.1', FILENAME)
    print name
    assert name == good_name
    assert os.path.exists(name)


def test_frozen():
    assert FROZEN is False


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
    assert (1, 2, 3) == vstr_2_vtuple('1.2.3')


def test_tuple_to_stirng():
    assert '1.2.3' == vtuple_2_vstr((1, 2, 3))
