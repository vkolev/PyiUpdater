import logging
import time

logger = logging.getLogger(__name__)

from pyi_updater.config import Config


# VERSION = (0, 9, 1, u'dev', int(time.time()))
VERSION = (0, 9, 0)


def get_version():
    version = '{}.{}'.format(VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '{}.{}'.format(version, VERSION[2])
    if len(VERSION) >= 4 and VERSION[3]:
        version = '{}-{}'.format(version, VERSION[3])
        if VERSION[3] == 'dev' and len(VERSION) >= 5 and VERSION[4] > 0:
            version = '{}{}'.format(version, VERSION[4])
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
