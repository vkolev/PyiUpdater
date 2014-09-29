import os
import shutil
import sys

from nose import with_setup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyi_updater import PyiUpdater
from pyi_updater.client import Client
from tconfig import TConfig

client = Client(TConfig(), test=True)


def tear_down():
    if os.path.exists(client.data_dir):
        shutil.rmtree(client.data_dir, ignore_errors=True)


def test_data_dir():
    client = Client(TConfig(), test=True)
    assert os.path.exists(client.data_dir) is True


def test_original_init():
    config = TConfig()
    updater = PyiUpdater(config)
    client = Client(updater, test=True)
    assert client.app_name == u'jms'
    assert client.update_urls[0] == (u'https://s3-us-west-1.amazon'
                                    'aws.com/pyi-test/')


def test_new_init():
    config = TConfig()
    client = Client(config, test=True)
    assert client.app_name == u'jms'
    assert client.update_urls[0] == (u'https://s3-us-west-1.amazon'
                                    'aws.com/pyi-test/')


def test_bad_pub_key():
    config = TConfig()
    config.PUBLIC_KEY = 'bad key'
    client = Client(config, test=True)
    assert client.update_check(u'jms', '0.0.0') is False


@with_setup(None, tear_down)
def test_check_version():
    config = TConfig()
    client = Client(config, test=True)
    assert client.update_check(client.app_name, '0.0.2') is True
    assert client.update_check(client.app_name, '6.0.0') is False


@with_setup(None, tear_down)
def test_failed_refresh_download():
    client = Client(None, test=True)
    assert client.download() is False


@with_setup(None, tear_down)
def test_download():
    client = Client(TConfig(), test=True)
    assert client.app_name == u'jms'
    assert client.update_check(client.app_name, '0.0.1') is True
    assert client.download() is True
    assert client.install() is True
