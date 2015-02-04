# --------------------------------------------------------------------------
# Copyright 2014 Digital Sapphire Development Team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# --------------------------------------------------------------------------
import logging
from logging.handlers import RotatingFileHandler
import os

log = logging.getLogger()

from appdirs import user_log_dir
from jms_utils.logger import log_format_string

try:
    from PyInstaller import VERSION as temp_version
    pyi_version = (temp_version[0], temp_version[1], temp_version[2])
except ImportError:
    pyi_version = (0, 0, 0)

from pyi_updater.config import PyiUpdaterConfig
from pyi_updater.exceptions import PyiUpdaterError
from pyi_updater.key_handler import KeyHandler
from pyi_updater.package_handler import PackageHandler
from pyi_updater import settings
from pyi_updater.uploader import Uploader

log.setLevel(logging.DEBUG)
fmt_str = log_format_string()
nh = logging.NullHandler()
nh.setLevel(logging.DEBUG)
log.addHandler(nh)

LOG_DIR = user_log_dir(settings.APP_NAME, settings.APP_AUTHOR)
LOG_FILENAME_DEBUG = os.path.join(LOG_DIR, settings.LOG_FILENAME_DEBUG)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

rh = RotatingFileHandler(LOG_FILENAME_DEBUG, backupCount=5,
                         maxBytes=500000)
rh.setLevel(logging.DEBUG)
rh.setFormatter(log_format_string())
log.addHandler(rh)


class PyiUpdater(object):
    """Processes, signs & uploads updates

        Kwargs:

            config (obj): config object
    """

    def __init__(self, config=None):
        self.config = PyiUpdaterConfig()
        if pyi_version < (2, 1):
                raise PyiUpdaterError('Must have at least PyInstaller v2.1',
                                      expected=True)
        if config is not None:
            self.update_config(config)

    def update_config(self, config):
        """Updates internal config

        Args:

            config (obj): config object
        """
        self.config.update_config(config)
        self._update(self.config)

    def _update(self, config):
        self.kh = KeyHandler(config)
        self.ph = PackageHandler(config)
        self.up = Uploader(config)

    def setup(self):
        """Sets up root dir with required PyiUpdater folders
        """
        self.ph.setup()

    def process_packages(self):
        """Creates hash for updates & adds information about update to
        version file
        """
        self.ph.process_packages()

    def set_uploader(self, requested_uploader):
        """Sets upload destination

        Args:

            requested_uploader (str): upload service. i.e. s3, scp
        """
        self.up.set_uploader(requested_uploader)

    def upload(self):
        """Uploads files in deploy folder
        """
        self.up.upload()

    def make_keys(self, count):
        """Creates signing keys
        """
        self.kh.make_keys(count)

    def revoke_key(self, count):
        self.kh.revoke_key(count)

    def get_recent_revoked_key(self):
        return self.kh.get_recent_revoked_key()

    def sign_update(self):
        "Signs version file with signing key"
        self.kh.sign_update()

    def get_public_keys(self):
        "Returns public key"
        return self.kh.get_public_keys()

    def print_public_key(self):
        "Prints public key to console"
        self.kh.print_public_key()

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
