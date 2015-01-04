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


import json
import os
import shutil
import urllib2

import pytest

from pyi_updater.patcher import Patcher

UPDATE_DIR = 'updates'
TEST_DATA_DIR = os.path.join('tests', 'test data', 'patcher-test-data')

version_file_url = 'https://s3-us-west-1.amazonaws.com/pyi-test/version.json'
json_data = json.loads(urllib2.urlopen(version_file_url).read())

update_data = {
    u'name': u'jms',
    u'json_data': json_data,
    u'current_version': u'0.0.1',
    u'highest_version': u'0.0.3',
    u'update_folder': UPDATE_DIR,
    u'update_urls': [u'https://s3-us-west-1.amazonaws.com/pyi-test/'],
    u'platform': u'mac',
    }


@pytest.fixture(scope='module')
def setup(request):
    def fin():
        if os.path.exists(UPDATE_DIR):
            shutil.rmtree(UPDATE_DIR, ignore_errors=True)

    if os.path.exists(UPDATE_DIR):
        shutil.rmtree(UPDATE_DIR)
    os.mkdir(UPDATE_DIR)

    base_binary = os.path.join(TEST_DATA_DIR, u'jms-mac-0.0.1.zip')
    shutil.copy(base_binary, UPDATE_DIR)
    request.addfinalizer(fin)


@pytest.fixture(scope='module')
def teardown(request):
    def fin():
        if os.path.exists(UPDATE_DIR):
            shutil.rmtree(UPDATE_DIR, ignore_errors=True)
    if not os.path.exists(UPDATE_DIR):
        os.mkdir(UPDATE_DIR)
    request.addfinalizer(fin)


def test_execution(setup):
    p = Patcher(**update_data)
    assert p.start() is True


def test_bad_hash_current_version(setup):
    bad_data = update_data.copy()
    bad_data['current_file_hash'] = u'Thisisabadhash'
    p = Patcher(**bad_data)
    assert p.start() is False


def test_no_base_binary(teardown):
    p = Patcher(**update_data)
    assert p.start() is False


def test_no_base_to_patch(teardown):
    p = Patcher(**update_data)
    assert p.start() is False


def test_missing_version(teardown):
    bad_data = update_data.copy()
    bad_data[u'highest_version'] = u'0.0.4'
    p = Patcher(**bad_data)
    assert p.start() is False
