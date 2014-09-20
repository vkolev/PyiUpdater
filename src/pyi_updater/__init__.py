import logging
import os

logger = logging.getLogger(__name__)

from pyi_updater.client import Client
from pyi_updater.config import Config
from pyi_updater.downloader import FileDownloader
from pyi_updater.exceptions import PyiUpdaterError
from pyi_updater.filecrypt import FileCrypt
from pyi_updater.key_handler import KeyHandler
from pyi_updater.package_handler import PackageHandler
from pyi_updater.patcher import Patcher
from pyi_updater.uploader import Uploader


class PyiUpdater(object):
    """There are 2 ways to load config.  The first was is during
    object initialization. The second way is later with :meth:`update_config`

    Examples are shown below::

        Config(object):
            APP_NAME = "NST"

            APP_DATA_DIR = None

            UPDATE_URL = http://www.test-nst.com/updates

        app = NotSoTuf(__name__, Config())

        app = NotSoTuf(__name__)
        app.update_config(Config())

    Kwargs:
        import_name (str): used to get current directory

        cfg_obj (instance): object with config attributes
    """
    def __init__(self, import_name=None, cfg_obj=None):
        if import_name is None:
            raise PyiUpdaterError(u'You have to pass __name__ to '
                                  'NotSoTuf(__name__)', expected=True)
        self.import_name = import_name
        self.real_path = os.path.dirname(os.path.abspath(self.import_name))
        self.config = Config()
        self.config['DEV_DATA_DIR'] = self.real_path
        if cfg_obj:
            self.update_config(cfg_obj)

    def update_config(self, obj):
        """Proxy method to update internal config dict

        Args:
            obj (instance): config object
        """
        self.config.from_object(obj)
        if self.config.get(u'APP_NAME', None) is None:
            self.config[u'APP_NAME'] = u'Pyi Updater App'
