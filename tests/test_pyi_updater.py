from pyi_updater import PyiUpdaterConfig

from tconfig import TConfig


def test_dev_dir_none():
    updater = PyiUpdaterConfig()
    myconfig = TConfig()
    myconfig.APP_NAME = None
    updater.update_config(myconfig)
    assert updater[u'APP_NAME'] == u'PyiUpdater App'
