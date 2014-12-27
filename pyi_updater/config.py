import logging
import os
import pickle


log = logging.getLogger(__name__)


class Loader(object):

    def __init__(self):
        self.cwd = os.getcwd()
        self.config_dir = os.path.join(self.cwd, u'.pyiupdater')
        self.config_file = os.path.join(self.config_dir, u'config.data')
        self.password = os.environ.get('PYIUPDATER_PASS')

    def load_config(self):
        log.debug(u'Loading config')
        try:
            with open(self.config_file, u'r') as f:
                config_data = pickle.loads(f.read())
        except Exception as e:
            log.error(e, exc_info=True)
            config_data = SetupConfig()
        return config_data

    def save_config(self, obj, password=None):
        log.debug('Saving Config')
        if not os.path.exists(self.config_dir):
            os.mkdir(self.config_dir)
        with open(self.config_file, u'w') as f:
            f.write(str(pickle.dumps(obj)))

        self.write_config_py(obj)

    def write_config_py(self, obj):
        filename = os.path.join(self.cwd, u'client_config.py')
        attr_str_format = "    {} = '{}'\n"
        attr_format = "    {} = {}\n"
        with open(filename, u'w') as f:
            # Temp hack for pyinstaller not finding pkg_resources
            f.write('import pkg_resources\n\n')
            f.write('class ClientConfig(object):\n')
            if hasattr(obj, 'APP_NAME') and obj.APP_NAME is not None:
                f.write(attr_str_format.format('APP_NAME', obj.APP_NAME))
            if hasattr(obj, 'COMPANY_NAME') and obj.COMPANY_NAME is not None:
                f.write(attr_str_format.format('COMPANY_NAME',
                        obj.COMPANY_NAME))
            if hasattr(obj, 'UPDATE_URLS') and obj.UPDATE_URLS is not None:
                f.write(attr_format.format('UPDATE_URLS', obj.UPDATE_URLS))
            if hasattr(obj, 'PUBLIC_KEY') and obj.PUBLIC_KEY is not None:
                f.write(attr_str_format.format('PUBLIC_KEY', obj.PUBLIC_KEY))


class PyiUpdaterConfig(dict):
    u"""Works exactly like a dict but provides ways to fill it from files
    or special dictionaries.  There are two common patterns to populate the
    config.

    You can define the configuration options in the
    module that calls :meth:`from_object`.  It is also possible to tell it
    to use the same module and with that provide the configuration values
    just before the call.

    Loading from modules, only uppercase keys are added to the config.
    This makes it possible to use lowercase values in the config file for
    temporary values that are not added to the config or to define the config
    keys in the same file that implements the application.
    """

    def __init__(self, obj=None):
        super(PyiUpdaterConfig, self).__init__(dict())
        if obj is not None:
            self.from_object(obj)

    def from_object(self, obj):
        u"""Updates the values from the given object

        Args:
            obj (instance): Object with config attributes

        Objects are classes.

        Just the uppercase variables in that object are stored in the config.
        Example usage::

            from yourapplication import default_config
            app.config.from_object(default_config())
        """
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)

    def update_config(self, obj):
        u"""Proxy method to update internal config dict

        Args:
            obj (instance): config object
        """
        self.from_object(obj)
        if self.get(u'APP_NAME') is None:
            self[u'APP_NAME'] = u'PyiUpdater App'
        if self.get(u'COMPANY_NAME') is None:
            self[u'COMPANY_NAME'] = u'Digital Sapphire'

    def __str__(self):
        return dict.__repr__(self)

    def __unicode__(self):
        pass

    def __repr__(self):
        return u'<%s %s>' % (self.__class__.__name__, dict.__repr__(self))


# This is the default config used
class SetupConfig(object):
    # If left None "Not_So_TUF" will be used
    APP_NAME = None

    # Company/Your name
    COMPANY_NAME = None

    # If set more debug info will be printed to console
    DEBUG = False

    # Public Key used by your app to verify update data
    # REQUIRED
    PUBLIC_KEY = None

    # Url to ping for updates
    UPDATE_URL = None

    # List of urls to ping for updates
    # REQUIRED
    UPDATE_URLS = None

    # Support for patch updates
    UPDATE_PATCHES = True

    # Upload Setup
    REMOTE_DIR = None
    HOST = None
    USERNAME = None
    PASSWORD = None
