import os

test_dir = os.path.join(os.path.abspath(os.getcwd()), u'tests')


class TConfig(object):
    bad_attr = u'bad attr'
    # If left None "Not_So_TUF" will be used
    APP_NAME = u'jms'

    # Directory for updater to place verified updates.
    # If left blank will be place in the users home
    # directory Unix ".Not_So_TUF"
    # windows "Not_So_Tuf"
    APP_DATA_DIR = os.path.join(test_dir, u'app_data')

    COMPANY_NAME = u'JMS LLC'

    # If True more debug info will be printed to console
    DEBUG = False

    # Work directory on dev machine for framework to
    # do its business. sign updates, get hashes etc...
    # If None a data folder will be created in the
    # current directory
    DEV_DATA_DIR = test_dir

    # Length of keys to sign and verify files with
    # If left None 2048 key size will be used
    KEY_LENGTH = 1024

    # Public Key used by your app to verify update data
    # REQUIRED
    PUBLIC_KEY = 'lnhgrbYJKubaLzjiKusMa1UU6i4aUe9gofzEkRm9F68'
    PUBLIC_KEYS = ['lnhgrbYJKubaLzjiKusMa1UU6i4aUe9gofzEkRm9F68']

    # Online repository where you host your packages
    # and version file
    # REQUIRED
    UPDATE_URL = u'https://s3-us-west-1.amazonaws.com/pyi-test/'
    UPDATE_PATCHES = True

    # Upload Setup
    REMOTE_DIR = None
    HOST = None

    # server user name/access key id
    USERNAME = None
    # Path to ssh key of server / password / secret access key
    PASSWORD = u'/path/to/ssh/key file'

    SERVER_CERT_VERIFY = True
