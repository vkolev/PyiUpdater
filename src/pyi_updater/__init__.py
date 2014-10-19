import logging
import time

logger = logging.getLogger(__name__)

try:
    from PyInstaller import VERSION as temp_version
    pyi_version = (temp_version[0], temp_version[1], temp_version[2])
except ImportError:
    pyi_version = (0, 0, 0)

from pyi_updater.config import Config
from pyi_updater.exceptions import PyiUpdaterError


if pyi_version < (2, 1, 1):
    raise PyiUpdaterError('Must have at least PyInstaller v2.1.1',
                          expected=True)

# VERSION = (0, 9, 2, u'dev', int(time.time()))
VERSION = (0, 9, 1)


def get_version():
    return _get_version(VERSION)


def _get_version(v):
    version = '{}.{}'.format(v[0], v[1])
    if v[2]:
        version = '{}.{}'.format(version, v[2])
    if len(VERSION) >= 4 and v[3]:
        version = '{}-{}'.format(version, v[3])
        if v[3] == 'dev' and len(VERSION) >= 5 and v[4] > 0:
            version = '{}{}'.format(version, v[4])
    return version


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
