import os
import shutil
import sys

from nose.tools import raises, with_setup

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)),
                u'src'))

from pyi_updater import PyiUpdater, Uploader
from pyi_updater.exceptions import UploaderError
from tconfig import TConfig

my_config = TConfig()

updater = PyiUpdater(__name__, my_config)
uploader = Uploader(updater)


def setup_func():
    if not os.path.exists(uploader.deploy_dir):
        os.makedirs(uploader.deploy_dir)


def teardown_func():
    if os.path.exists(uploader.deploy_dir):
        shutil.rmtree(os.path.dirname(uploader.deploy_dir))


@raises(UploaderError)
def test_set_uploader_int_param():
    uploader.set_uploader(1)


@with_setup(setup_func, teardown_func)
@raises(UploaderError)
def test_set_uploader_no_s3_settings():
    uploader.set_uploader(u's3')


@raises(UploaderError)
def test_set_uploader_invalid_str():
    uploader.set_uploader(u'data')


@raises(UploaderError)
def test_upload_not_ready():
    uploader.uploader = None
    uploader.upload()


@raises(UploaderError)
def test_set_uploader_bad_settings():
    config = TConfig()
    config.ACCESS_KEY_ID = None
    config.SECRET_ACCESS_KEY = u'Not an actual secret'
    config.BUCKET_NAME = u'Bucket Name'
    s_nst = PyiUpdater(__name__, config)
    uploader = Uploader(s_nst)
    uploader.set_uploader(u's3')
