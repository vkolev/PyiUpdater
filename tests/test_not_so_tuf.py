import os
import sys

from nose.tools import raises

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyi_updater import PyiUpdater
from pyi_updater.exceptions import PyiUpdaterError

from tconfig import TConfig


@raises(PyiUpdaterError)
def test_name_fail():
    updater = PyiUpdater()


def test_dev_dir():
    updater = PyiUpdater(__name__)
    assert updater.real_path == updater.config[u'DEV_DATA_DIR']


def test_dev_dir_none():
    updater = PyiUpdater(__name__)
    myconfig = TConfig()
    myconfig.APP_NAME = None
    updater.update_config(myconfig)
    assert updater.config[u'APP_NAME'] == u'Pyi Updater App'
