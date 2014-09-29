import sys

from pyi_updater import PyiUpdater
from pyi_updater.key_handler import KeyHandler
from pyi_updater.package_handler import PackageHandler


# Not So TUF handles configuration with simple
# class attributes.  They must be in all CAPS.
# to be registered.  You may pass in custom
# settings to be used later.
class DefaultConfig(object):
    # If left None "Not_So_TUF" will be used
    APP_NAME = None

    # Length of keys to sign and verify files with
    # If left None 2048 key size will be used
    KEY_LENGTH = None

    # Name made for your private key. If left
    # None "Not_So_TUF.pem" will be used
    PRIVATE_KEY_NAME = None

    # Public Key used by your app to verify update data
    # REQUIRED
    PUBLIC_KEY = (17022351873105053147088163105983577257966692560663543347938383809747979750470266069914732864252844768385355907146386077123799054565611846357055920249193620195180631869615743769334796990192318489812142889414970955334254855590299723893423021589397127184769063465102962682096447452967415650677942469205402943507368208858916471188750637174661509489946569932170884064066442273331420184865693888703840905553949492223898597770128267763408408345292193296577459922276202765690561166119202208933879945227147091774656864580608582752643190913932634012968436576443560457625241838298968657806362615969869008716434463574851608691099L, 65537)

    # Name made for your public key.  If left
    # None "Not_So_TUF.pub" will be used
    PUBLIC_KEY_NAME = None

    # Online repository where you host your packages
    # and version file
    # REQUIRED
    UPDATE_URL = 'https://s3-us-west-1.amazonaws.com/not-so-tuf/'
    UPDATE_PATCHES = True

    # Upload Setup
    REMOTE_DIR = None
    HOST = None
    USERNAME = None
    PASSWORD = None


def setup():
    # Setting up Config object
    default_config = DefaultConfig()

    # Initilizing Main object and configuring
    # in one step
    pyi = PyiUpdater(default_config)

    # Can also update config later
    pyi.update_config(default_config)

    # Setting up Package Handler
    # Getting config from updater
    package_handler = PackageHandler(pyi)

    # Setting up work directories
    # Only need to run once but ok
    # if ran multipule times
    package_handler.setup()

    # Now place new packages in the folder named
    # "new" in the data directory
    raw_input('Place updates in new folder then press enter.')
    # This updates the version file with the
    # new packages
    package_handler.update_package_list()

    # Initializing KeyHandler and getting
    # config from updater
    key_handler = KeyHandler(pyi)

    # After you have updated your package
    # list sign your package list
    key_handler.sign_update()

    # Now copies your packages to their
    # "files" directory by name and version
    # number.
    # Also moves files from the new folder to
    # deploy folder ready for uploading
    package_handler.deploy()


def make_keys():
    default_config = DefaultConfig()
    pyi = PyiUpdater(default_config)
    key_handler = KeyHandler(pyi)
    # Making a new set of keys
    # Keys will be place in the keys
    # Directory, in the data folder
    # ** Should not be ran again after
    # ** you deploy your app!!!! **
    # TODO: support multiple keys
    key_handler.make_keys()


def main():
    ans = raw_input('1. Setup\n2. Make Keys\n*. Exit\n-->')
    if ans == '1':
        setup()
    elif ans == '2':
        make_keys()
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()
