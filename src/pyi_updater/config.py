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
            app.config.from_object(default_config)
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


class SetupConfig(object):
    # If left None "Not_So_TUF" will be used
    APP_NAME = None

    # Company/Your name
    COMPANY_NAME = None

    # Directory for updater to place verified updates.
    APP_DATA_DIR = None

    # If set more debug info will be printed to console
    DEBUG = False

    # Work directory on dev machine for framework to
    # do its business. sign updates, get hashes etc...
    # If None a data folder will be created in the
    # current directory
    DEV_DATA_DIR = None

    # Length of keys to sign and verify files with
    # If left None 2048 key size will be used
    KEY_LENGTH = None

    # Name made for your private key. If left
    # None "Not_So_TUF.pem" will be used
    PRIVATE_KEY_NAME = None

    # Public Key used by your app to verify update data
    # REQUIRED
    PUBLIC_KEY = None

    # Name made for your public key.  If left
    # None "Not_So_TUF.pub" will be used
    PUBLIC_KEY_NAME = None

    # Online repository where you host your packages
    # and version file
    # REQUIRED
    UPDATE_URL = None

    # Support for patch updates
    UPDATE_PATCHES = True

    # Upload Setup
    REMOTE_DIR = None
    HOST = None

    USERNAME = None
    PASSWORD = None
    SSH_KEY_PATH = u''
