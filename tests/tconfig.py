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

    # Name made for your private key. If left
    # None "Not_So_TUF.pem" will be used
    PRIVATE_KEY_NAME = None

    # Public Key used by your app to verify update data
    # REQUIRED
    PUBLIC_KEY = (22628297174438195198671246916007838449214750475314443890601800651781620871630489972447885717534744145991607088614294495842260935046991596946657467583417502903716510054581869782504552359073077898335574455852269558914319229780765420082847986287083104804068678544842021448782974669569122308730193328218585602474058305882046631453437027512060726647640447504544237822097147849770932725391520447470558959586315489069320819900473440371982304306982817768634747817357796616411085701648034588919506109670201650765184639261926301209670835655036196469799239760964221276924987720731147231765552998517326286415757085736015695313247L, 65537L)

    # Name made for your public key.  If left
    # None "Not_So_TUF.pub" will be used
    PUBLIC_KEY_NAME = None

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
