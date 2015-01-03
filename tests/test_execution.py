import os
import sys
import shutil

from jms_utils.paths import ChDir
from nose import with_setup

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pyi_updater import PyiUpdaterConfig
from pyi_updater.key_handler import KeyHandler
from pyi_updater.package_handler import PackageHandler
from pyi_updater.utils import remove_dot_files

from tconfig import TConfig

pyi_config = PyiUpdaterConfig(TConfig())
kh = KeyHandler(pyi_config)
kh.test = True
ph = PackageHandler(pyi_config)

PYI_DATA = os.path.abspath(os.path.join(u'tests', u'pyi-data'))


def setup_func():
    ph.setup()
    kh.make_keys()
    test_data_dir = os.path.abspath(os.path.join(u'tests', u'test data',
                                    u'5.0'))
    with ChDir(test_data_dir):
        files = remove_dot_files(os.listdir(os.getcwd()))
        for f in files:
            shutil.copy(f, ph.new_dir)
    ph.process_packages()
    kh.sign_update()


def teardown_func():
    path = os.path.join(u'.pyiupdater')
    with ChDir(u'tests'):
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)


@with_setup(setup_func, teardown_func)
def test_exe1():
    assert os.path.exists(ph.new_dir) is True
    assert os.path.exists(ph.deploy_dir) is True


# @with_setup(None, teardown_func)
# def test_patch_creation():
#     test_data_dir = os.path.abspath(os.path.join(u'tests', u'test data',
#                                     u'5.3'))
#     with ChDir(test_data_dir):
#         files = remove_dot_files(os.listdir(os.getcwd()))
#         for f in files:
#             shutil.copy(f, ph.new_dir)
#     ph.process_packages()
#     kh.sign_update()
#     assert os.path.exists(os.path.join(PYI_DATA, u'deploy',
#                           u'Not So TUF-arm-101')) is True
#     assert os.path.exists(os.path.join(PYI_DATA, u'deploy',
#                           u'Not So TUF-mac-101')) is True


def test_move_to_deploy():
    deploy_dir = os.path.join(PYI_DATA, u'deploy')
    with ChDir(deploy_dir):
        files = os.listdir(os.getcwd())
        assert u'version.json' in files
        assert u'Not So TUF-arm-0.5.0.zip' in files
        assert u'Not So TUF-mac-0.5.0.zip' in files
        # assert u'Not So TUF-arm-0.5.3.zip' in files
        # assert u'Not So TUF-mac-0.5.3.zip' in files
