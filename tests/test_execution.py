import os
from nose import with_setup
import shutil
import sys

from jms_utils import ChDir

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyi_updater import KeyHandler, PackageHandler, PyiUpdater
from pyi_updater.utils import remove_dot_files

from tconfig import TConfig

pyi_updater = PyiUpdater(__name__, TConfig())
kh = KeyHandler(pyi_updater)
kh.test = True
kh._add_filecrypt()
ph = PackageHandler(pyi_updater)

nst_data = os.path.abspath(os.path.join(u'tests', u'pyi-data'))


def setup_func():
    ph.setup()
    kh.make_keys()
    test_data_dir = os.path.abspath(os.path.join(u'tests', u'test data',
                                    u'5.0'))
    with ChDir(test_data_dir):
        files = remove_dot_files(os.listdir(os.getcwd()))
        for f in files:
            shutil.copy(f, ph.new_dir)
    ph.update_package_list()
    kh.sign_update()
    ph.deploy()


@with_setup(setup_func, None)
def test_exe1():
    assert os.path.exists(nst_data) is True


def setup_func2():
    test_data_dir = os.path.abspath(os.path.join(u'tests', u'test data',
                                    u'5.3'))
    with ChDir(test_data_dir):
        files = remove_dot_files(os.listdir(os.getcwd()))
        for f in files:
            shutil.copy(f, ph.new_dir)
    ph.update_package_list()
    kh.sign_update()
    ph.deploy()


@with_setup(setup_func2, None)
def test_exe2():
    assert os.path.exists(nst_data) is True


def test_patch_creation():
    assert os.path.exists(os.path.join(nst_data, u'deploy',
                          u'Not So TUF-arm-2')) is True
    assert os.path.exists(os.path.join(nst_data, u'deploy',
                          u'Not So TUF-mac-2')) is True


def test_move_to_deploy():
    deploy_dir = os.path.join(nst_data, u'deploy')
    with ChDir(deploy_dir):
        files = os.listdir(os.getcwd())
        assert u'version.json' in files
        assert u'Not So TUF-arm-0.5.0.zip' in files
        assert u'Not So TUF-mac-0.5.0.zip' in files
        assert u'Not So TUF-arm-0.5.3.zip' in files
        assert u'Not So TUF-mac-0.5.3.zip' in files
