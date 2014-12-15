import os
import shutil

from nose import with_setup

from pyi_updater.client import Client
from tconfig import TConfig

client = Client(TConfig(), test=True)


def tear_down():
    if os.path.exists(client.data_dir):
        shutil.rmtree(client.data_dir, ignore_errors=True)


def test_data_dir():
    client = Client(TConfig(), test=True)
    assert os.path.exists(client.data_dir) is True


def test_new_init():
    client = Client(TConfig(), refresh=True, test=True)
    assert client.app_name == u'jms'
    assert client.update_urls[0] == (u'https://s3-us-west-1.amazon'
                                     'aws.com/pyi-test/')


def test_no_cert():
    client = Client(TConfig(), refresh=True, test=True)
    client.verify = False
    assert client.app_name == u'jms'
    assert client.update_urls[0] == (u'https://s3-us-west-1.amazon'
                                     'aws.com/pyi-test/')


def test_bad_pub_key():
    config = TConfig()
    config.PUBLIC_KEY = 'bad key'
    client = Client(config, refresh=True, test=True)
    assert client.update_check(u'jms', '0.0.0') is None


@with_setup(None, tear_down)
def test_check_version():
    client = Client(TConfig(), refresh=True, test=True)
    assert client.update_check(client.app_name, '0.0.2') is not None
    assert client.update_check(client.app_name, '6.0.0') is None


@with_setup(None, tear_down)
def test_failed_refresh_download():
    client = Client(None, refresh=True, test=True)
    assert client.ready is False


@with_setup(None, tear_down)
def test_download():
    client = Client(TConfig(), refresh=True, test=True)
    update = client.update_check(client.app_name, '0.0.1')
    assert update is not None
    assert update.app_name == u'jms'
    assert update.download() is True
    assert update.is_downloaded() is True
    assert update.extract() is True
