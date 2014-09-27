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
    'name': 'jms',
    'json_data': json_data,
    'current_version': '0.0.1',
    'highest_version': '0.0.2',
    'update_folder': UPDATE_DIR,
    'update_url': 'https://s3-us-west-1.amazonaws.com/pyi-test/',
    'platform': 'mac',
    }


def setup():
    if os.path.exists(UPDATE_DIR):
        shutil.rmtree(UPDATE_DIR)
    os.mkdir(UPDATE_DIR)

    base_binary = os.path.join(TEST_DATA_DIR, 'jms-mac-0.0.1.zip')
    shutil.copy(base_binary, UPDATE_DIR)


def teardown():
    if os.path.exists(UPDATE_DIR):
        shutil.rmtree(UPDATE_DIR)


@with_setup(setup, teardown)
def test_execution():
    p = Patcher(**update_data)
    assert p.start() is True
