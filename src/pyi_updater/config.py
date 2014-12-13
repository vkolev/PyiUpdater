class Config(dict):
    """Works exactly like a dict but provides ways to fill it from files
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

    def __init__(self, defaults=None):
        super(Config, self).__init__(defaults or {})

    def from_object(self, obj):
        """Updates the values from the given object

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

    def __str__(self):
        pass

    def __unicode__(self):
        pass

    def __repr__(self):
        return u'<%s %s>' % (self.__class__.__name__, dict.__repr__(self))


class PyiUpdaterConfig(object):
    """There are 2 ways to load config.  The first was is during
    object initialization. The second way is later with :meth:`update_config`

    Examples are shown below::

        Config(object):
            APP_NAME = "My App"
            COMPANY_NAME = "MY COMPANY"
            UPDATE_URL = http://www.example.com/updates


        app = PyiUpdater(Config())

        app = PyInstaller()
        app.update_config(Config())

    Kwargs:
        import_name (str): used to get current directory

        cfg_obj (instance): object with config attributes
    """
    def __init__(self, cfg_obj=None):
        self.config = Config()
        if cfg_obj is not None:
            self.update_config(cfg_obj)

    def update_config(self, obj):
        """Proxy method to update internal config dict

        Args:
            obj (instance): config object
        """
        self.config.from_object(obj)
        if self.config.get(u'APP_NAME', None) is None:
            self.config[u'APP_NAME'] = u'PyiUpdater App'


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
