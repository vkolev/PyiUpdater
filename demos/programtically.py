from pyi_updater import PyiUpdater
from pyi_updater.key_handler import KeyHandler
from pyi_updater.package_handler import PackageHandler


# PyiUpdater handles configuration with simple
# class attributes.  They must be in all CAPS.
# to be registered.  You may pass in custom
# settings to be used later.
class DefaultConfig(object):
    # If left None "PyiUpdater App" will be used
    APP_NAME = "My New App"

    Company_Name = "Acme"

    # Used for verion file signature verification
    PUBLIC_KEY = (17022351873105053147088163105983577257966692560663543347938383809747979750470266069914732864252844768385355907146386077123799054565611846357055920249193620195180631869615743769334796990192318489812142889414970955334254855590299723893423021589397127184769063465102962682096447452967415650677942469205402943507368208858916471188750637174661509489946569932170884064066442273331420184865693888703840905553949492223898597770128267763408408345292193296577459922276202765690561166119202208933879945227147091774656864580608582752643190913932634012968436576443560457625241838298968657806362615969869008716434463574851608691099L, 65537)

    # Online repository where you host your packages
    # and version file
    UPDATE_URL = 'https://acme.com/updates'
    # List of urls to check if version file & update data
    # For each object need the urls will be used in succession
    # until the required object is found
    UPDATE_URLS = ['https://acme.com/updates',
                   'https://mirror.acme.com/updates',
                   'https://acme.amazon.com/updates']
    UPDATE_PATCHES = True

    # This is a path on the remote server or bucket name
    # on amazon s3
    REMOTE_DIR = "my-new-bucket"

    # The url or ip to remote host server.
    # Mostly for scp uploads
    HOST = None

    # Username or access ID
    USERNAME = None

    # Password or path to keyfile if using scp
    PASSWORD = None


def main():
    # Setting up Config object
    default_config = DefaultConfig()

    # Initilizing Main object and configuring
    # in one step
    pyi = PyiUpdater(default_config)

    # Can also update config later
    pyi.update_config(default_config)

    # Initializing Package Handler & Key Handler
    # with config info
    package_handler = PackageHandler(pyi)
    key_handler = KeyHandler(pyi)

    # Can also be Initilized without config
    package_handler = PackageHandler()
    key_handler = KeyHandler()

    # Then update handlers with config later
    package_handler.init_app(pyi)
    key_handler.init_app(pyi)

    # Setting up work directories
    # Only need to run once on a new project but it's
    # ok if ran multipule times
    package_handler.setup()
    key_handler.make_keys()

    # Now place new packages in the folder named
    # "new" in the pyi-data directory
    # Package Archive filename should be in the form
    # AppName-platform-version.zip
    raw_input('Place updates in new folder then press enter.')
    # This updates the version file with the
    # new packages & moves them to the deploy folder.
    package_handler.process_packages()

    # This signs the update manifest & copies it
    # to the deploy folder
    key_handler.sign_update()

if __name__ == '__main__':
    main()
