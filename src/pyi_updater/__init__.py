import logging
import time

logger = logging.getLogger(__name__)

try:
    from PyInstaller import VERSION as temp_version
    pyi_version = (temp_version[0], temp_version[1], temp_version[2])
except ImportError:
    pyi_version = (0, 0, 0)

from pyi_updater.config import PyiUpdaterConfig
from pyi_updater.exceptions import PyiUpdaterError
from pyi_updater.key_handler import KeyHandler
from pyi_updater.package_handler import PackageHandler
from pyi_updater.uploader import Uploader


def _get_version(v):
    version = '{}.{}'.format(v[0], v[1])
    if v[2]:
        version = '{}.{}'.format(version, v[2])
    if len(v) >= 4 and v[3]:
        version = '{}-{}'.format(version, v[3])
        if v[3] == 'dev' and len(v) >= 5 and v[4] > 0:
            version = '{}{}'.format(version, v[4])
    return version


def get_build():
    total = ''
    a = time.localtime(time.time())
    # total += str(a.tm_year)[2:]
    total += str(a.tm_mon)
    total += str(a.tm_mday)
    total += str(a.tm_hour)
    total += str(a.tm_min)
    return total

VERSION = (0, 13, 0, u'dev', get_build())
# VERSION = (0, 13, 0)


def get_version():
    return _get_version(VERSION)


class PyiUpdater(object):

    def __init__(self, config=None):
        self.config = PyiUpdaterConfig()
        if pyi_version < (2, 1, 1):
                raise PyiUpdaterError('Must have at least PyInstaller v2.1.1',
                                      expected=True)
        if config is not None:
            self.init(config)

    def init(self, config):
        self.update_config(config)

    def update_config(self, config):
        self.config.update_config(config)
        self._update(self.config)

    def _update(self, config):
        self.kh = KeyHandler(config)
        self.ph = PackageHandler(config)
        self.up = Uploader(config)

    def setup(self):
        self.ph.setup()

    def process_packages(self):
        self.ph.process_packages()

    def set_uploader(self, requested_uploader):
        self.up.set_uploader(requested_uploader)

    def upload(self):
        self.up.upload()

    def add_filecrypt(self, fc):
        self.kh.add_filecrypt(fc)

    def make_keys(self):
        self.kh.make_keys()

    def sign_update(self):
        self.kh.sign_update()

    def get_public_key(self):
        self.kh.get_public_key()

    def copy_decrypted_private_key(self):
        self.kh.copy_decrypted_private_key()

    def print_public_key(self):
        self.kh.print_public_key()
