import json
import os
import shutil
import sys

import ed25519
from jms_utils.paths import ChDir
from nose.tools import with_setup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyi_updater import PyiUpdaterConfig
from pyi_updater.key_handler import KeyHandler
from pyi_updater.package_handler import PackageHandler

from tconfig import TConfig

test_dir = u'tests'
data_dir = u'pyi-data'
test_data_dir = os.path.join(test_dir, data_dir)
keys_dir = os.path.join(test_data_dir, u'keys')
new_folder = os.path.join(test_data_dir, u'new')
version_file = os.path.join(test_data_dir, u'version.json')
pub_key = None


def setup_func():
    global test_data_dir

    config = TConfig()
    updater = PyiUpdaterConfig(config)
    ph = PackageHandler(updater)
    kh = KeyHandler(updater)
    kh.test = True
    ph.setup()
    kh.make_keys()


def teardown_func():
    with ChDir(u'tests'):
        shutil.rmtree(u'pyi-data', ignore_errors=True)


def setup_func2():
    global pub_key
    global test_data_dir

    config = TConfig()
    updater = PyiUpdaterConfig(config)
    ph = PackageHandler(updater)
    kh = KeyHandler(updater)

    ph.setup()
    kh.test = True
    kh.make_keys()
    pub_key = kh.get_public_key()

    # Make zipfile
    with ChDir(test_data_dir):
        os.mkdir(u'test-app')
        with ChDir(u'test-app'):
            with open(u'app.txt', u'w') as f:
                f.write(u'I am so happy' * 1000)
        shutil.make_archive(u'Test App-mac-0.2.0', u'zip', u'test-app')
        shutil.move(u'Test App-mac-0.2.0.zip', u'new')
    ph.process_packages()
    kh.sign_update()


def test_setup():
    global test_data_dir

    config = TConfig()
    updater = PyiUpdaterConfig(config)
    ph = PackageHandler(updater)
    key_dir = os.path.join(ph.data_dir, u'keys')

    kh = KeyHandler(updater)
    kh.test = True
    assert os.path.exists(os.path.abspath(key_dir))
    assert kh.private_key_name == u'jms.pem'
    assert kh.public_key_name == u'jms.pub'


@with_setup(setup_func2, teardown_func)
def test_key_verify():
    global pub_key
    global version_file

    with open(version_file) as vf:
        version_data = json.loads(vf.read())
    sig = version_data[u'sig']
    del version_data[u'sig']
    version_data = json.dumps(version_data, sort_keys=True)
    verify_key = ed25519.VerifyingKey(pub_key, encoding="base64")
    verify_key.verify(sig, version_data, encoding='base64')


@with_setup(setup_func, teardown_func)
def test_keydir_creation():
    global keys_dir
    assert os.path.exists(keys_dir) is True


@with_setup(setup_func, teardown_func)
def test_key_creation():
    global keys_dir
    files = os.listdir(keys_dir)
    # Names are generated from tconfig
    # extensions .pub and .pem are added
    # to appname if public and private key
    # key names are not provided in tconfig
    assert u'jms.pub' in files
    assert u'jms.pem' in files


@with_setup(None, teardown_func)
def test_execution():
    global test_data_dir

    config = TConfig()
    updater = PyiUpdaterConfig(config)
    ph = PackageHandler(updater)
    kh = KeyHandler(updater)

    ph.setup()
    kh.test = True
    kh.make_keys()

    # Make zipfile
    with ChDir(test_data_dir):
        os.mkdir(u'test-app')
        with ChDir(u'test-app'):
            with open(u'app.txt', u'w') as f:
                f.write(u'I am so happy' * 1000)
        shutil.make_archive(u'Test App-mac-0.2.0', u'zip', u'test-app')
        shutil.move(u'Test App-mac-0.2.0.zip', u'new')
    ph.process_packages()
    kh.sign_update()
