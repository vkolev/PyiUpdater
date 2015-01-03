import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pyi_updater import PyiUpdaterConfig

from tconfig import TConfig


def test_dev_dir_none():
    updater = PyiUpdaterConfig()
    myconfig = TConfig()
    myconfig.APP_NAME = None
    updater.update_config(myconfig)
    assert updater[u'APP_NAME'] == u'PyiUpdater App'
