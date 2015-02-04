# --------------------------------------------------------------------------
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
# --------------------------------------------------------------------------
import os
import shutil

from nose.tools import raises, with_setup

from pyi_updater import PyiUpdaterConfig
from pyi_updater.exceptions import UploaderError
from pyi_updater.uploader import Uploader
from pyi_updater.uploader.common import BaseUploader

from tconfig import TConfig

my_config = TConfig()

updater = PyiUpdaterConfig(my_config)
uploader = Uploader(updater)


def test_baseuploader_variables():
    base = BaseUploader()
    assert len(base.failed_uploads) == 0
    assert base.deploy_dir is None


@raises(NotImplementedError)
def test_baseuploader_init():
    base = BaseUploader()
    base.init()


@raises(NotImplementedError)
def test_baseuploader_connect():
    base = BaseUploader()
    base._connect()


@raises(NotImplementedError)
def test_baseuploader_upload_file():
    base = BaseUploader()
    base._upload_file('test')


def test_baseuploader_upload():
    base = BaseUploader()
    base.file_list = []
    base.upload() is True


@raises(NotImplementedError)
def test_baseuploader_upload_fail():
    base = BaseUploader()
    base.file_list = ['f']
    base.upload() is True


def test_baseuploader_retry_upload():
    base = BaseUploader()
    base._retry_upload() is True


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
    pyiconfig = PyiUpdaterConfig(config)
    uploader = Uploader(pyiconfig)
    uploader.set_uploader(u's3')
