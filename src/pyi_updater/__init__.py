import logging

logger = logging.getLogger(__name__)

from jms_utils.version import _get_version, get_build

try:
    from PyInstaller import VERSION as temp_version
    pyi_version = (temp_version[0], temp_version[1], temp_version[2])
except ImportError:
    pyi_version = (0, 0, 0)

from pyi_updater.config import Config
from pyi_updater.exceptions import PyiUpdaterError


# VERSION = (0, 10, 0, u'dev', get_build())
VERSION = (0, 10, 0)


def get_version():
    return _get_version(VERSION)


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
    def __init__(self, cfg_obj=None):
        if pyi_version < (2, 1, 1):
            raise PyiUpdaterError('Must have at least PyInstaller v2.1.1',
                                  expected=True)
        self.config = Config()
        if cfg_obj:
            self.update_config(cfg_obj)

    def update_config(self, obj):
        """Proxy method to update internal config dict

        Args:
            obj (instance): config object
        """
        self.config.from_object(obj)
        if self.config.get(u'APP_NAME', None) is None:
            self.config[u'APP_NAME'] = u'PyiUpdater App'
