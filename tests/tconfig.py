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
    PUBLIC_KEY = (22057311503871991036694098173498533391959787051502122245376968480944645335445711147926593963754167253694116700578731074529310461932744821112981849251334174660147886208826871329076579089247796943077424681271067884098601751761075857249990054983988244010443063133331815765037807026303433587120803683679078018854199695030385192114954291485123582999953828802798386987113599840294205767723335002960903764727549466683999990438810432137760573544215445312583436777736775764482964139950578026674795768382844206749763525494593165541092703395175712524665379250728145818970412810059082032765350774757096730729012833861991946387949L, 65537L)

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
