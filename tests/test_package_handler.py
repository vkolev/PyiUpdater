from nose import with_setup
from nose.tools import raises
import os
import shutil

from jms_utils.paths import ChDir

from pyi_updater import PyiUpdaterConfig
from pyi_updater.exceptions import PackageHandlerError
from pyi_updater.package_handler import PackageHandler
from pyi_updater.utils import count_contents

from tconfig import TConfig


def setup_func():
    config = TConfig()
    updater = PyiUpdaterConfig(config)
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


def setup_dir():
    os.mkdir('count-test')
    with ChDir('count-test'):
        count = 0
        while count < 4:
            with open(str(count), u'w') as f:
                f.write('A test')
            count += 1


def teardown_dir():
    if os.path.exists('count-test'):
        shutil.rmtree('count-test', ignore_errors=True)


@with_setup(setup_dir, teardown_dir)
def test_count_contents():
    assert count_contents('count-test') == 4
