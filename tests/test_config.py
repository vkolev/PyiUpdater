import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pyi_updater.config import PyiUpdaterConfig


class DevConfig(object):
    TESTING = True
    TEST_LOVE = True
    MORE_INFO = u'No Thanks'
    Bad_Attr = True


class ProdConfig(object):
    TESTING = False
    DEBUG = False
    MORE_INFO = u'Yes Please'


class BasicCofig(object):
    APP_NAME = u'Tester'


def test_dev_config():
    config = PyiUpdaterConfig()
    test_config = DevConfig()
    config.from_object(test_config)
    assert config[u'TESTING'] is True


def test_dev_config_bad_attr():
    config = PyiUpdaterConfig()
    test_config = DevConfig()
    config.from_object(test_config)
    assert config.get(u'BAD_ATTR', None) is None


def test_prod_config():
    config = PyiUpdaterConfig()
    prod_config = ProdConfig()
    config.from_object(prod_config)
    assert config[u'MORE_INFO'] == u'Yes Please'


def test_prod_bad_atter():
    test_prod_config()
    config = PyiUpdaterConfig()
    prod_config = ProdConfig()
    config.from_object(prod_config)
    assert config.get(u'DEBUG', None) is not None


def test_config_str():
    config = PyiUpdaterConfig()
    config.from_object(BasicCofig())
    assert repr(config) == u"<PyiUpdaterConfig {'APP_NAME': u'Tester'}>"
