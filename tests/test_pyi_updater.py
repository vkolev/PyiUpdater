import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyi_updater import PyiUpdater

from tconfig import TConfig


def test_dev_dir_none():
    updater = PyiUpdater(__name__)
    myconfig = TConfig()
    myconfig.APP_NAME = None
    updater.update_config(myconfig)
    assert updater.config[u'APP_NAME'] == u'PyiUpdater App'
