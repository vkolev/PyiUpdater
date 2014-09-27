import json
import os
import shutil
import sys
import urllib2

from nose.tools import with_setup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
    u'update_url': u'https://s3-us-west-1.amazonaws.com/pyi-test/',
    u'platform': u'mac',
    }


def setup():
    if os.path.exists(UPDATE_DIR):
        shutil.rmtree(UPDATE_DIR)
    os.mkdir(UPDATE_DIR)

    base_binary = os.path.join(TEST_DATA_DIR, u'jms-mac-0.0.1.zip')
    shutil.copy(base_binary, UPDATE_DIR)


def teardown():
    if os.path.exists(UPDATE_DIR):
        shutil.rmtree(UPDATE_DIR)


@with_setup(setup, teardown)
def test_execution():
    p = Patcher(**update_data)
    assert p.start() is True


@with_setup(setup, teardown)
def test_bad_hash_current_version():
    bad_data = update_data.copy()
    bad_data['current_file_hash'] = u'Thisisabadhash'
    p = Patcher(**bad_data)
    assert p.start() is False


@with_setup(None, teardown)
def test_no_base_binary():
    os.mkdir(UPDATE_DIR)
    p = Patcher(**update_data)
    assert p.start() is False


@with_setup(None, teardown)
def test_no_base_to_patch():
    os.mkdir(UPDATE_DIR)
    p = Patcher(**update_data)
    assert p.start() is False


@with_setup(setup, teardown)
def test_missing_version():
    bad_data = update_data.copy()
    bad_data[u'highest_version'] = u'0.0.4'
    p = Patcher(**bad_data)
    assert p.start() is False
