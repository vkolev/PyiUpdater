from nose import with_setup
from nose.tools import raises
import os
import shutil
import sys

from jms_utils.paths import ChDir

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyi_updater import PyiUpdater
from pyi_updater.exceptions import PackageHandlerError
from pyi_updater.package_handler import PackageHandler

from tconfig import TConfig


def setup_func():
    config = TConfig()
    updater = PyiUpdater(config)
    ph = PackageHandler(updater)
    ph.setup()


def teardown_func():
    with ChDir('tests'):
        if os.path.exists(u'pyi-data'):
            shutil.rmtree(u'pyi-data', ignore_errors=True)
        if os.path.exists(u'.pyiupdater'):
            shutil.rmtree(u'.pyiupdater')


@with_setup(setup_func, teardown_func)
def test_folder_layout():
    with ChDir(u'tests'):
        assert os.path.exists(u'pyi-data') is True

    with ChDir(u'tests/pyi-data'):
        assert os.path.exists(u'new') is True
        assert os.path.exists(u'deploy') is True
        assert os.path.exists(u'files') is True


@raises(PackageHandlerError)
def test_process_packages_no_init():
    ph = PackageHandler()
    ph.process_packages()
