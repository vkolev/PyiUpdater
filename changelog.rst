v0.13.0 - develop
~~~~~~~~~~~~~~~~~~~
.. note:: This version is not yet released and is under active development.

Backwards incompatible release
------------------------------
Demos have been update with the changes. Also its very important to make a decrypted copy of your config file before updating.
============================

* Updated

  - CLI

    - Updated with subcommands
    - pyiupdater -h
    - pyiupdater command -h

  - PyiUpdater

    - Simplified config

* Fixed

  - PyiUpdater

    - Logging when pyi.log is next to Mac .app bundles

* Removed

  - Client

    - Redundant code

  - FileCrypt

    - Passwords for remote locations will need to be set as env vars

  - PyiUpdater

    - Redundant system calls

  - TUI

    - Removed in favor of cli


v0.12.3 - 2014/12/7
~~~~~~~~~~~~~~~~~~~
* Updated

  - Client

    - Handling version numbers passed to update_check

* Fixed

  - Client

    - Missing var

  - PackageHandler

    - Incrementing patch number
    - Trying to move a file that doesn't exist
    - Doing migrate on every run
    - Getting hash of file that doesn't exists

v0.12.2 - 2014/12/7
~~~~~~~~~~~~~~~~~~~
* Updated

  - PackageHandler

    - Error reporting when calling methods

* Fixed

  - CLI scripts

* Removed

  - Some unused code

v0.12.1 - 2014/12/4
~~~~~~~~~~~~~~~~~~~
* Fixed

  - Migrating to new patch numbering system


v0.12.0 - 2014/11/29
~~~~~~~~~~~~~~~~~~~~

* Added

  - .pyiupdater data directory. Used to keep track of packages & patch numbers.

* Updated

  - PackageHandler

    - Will migrate packages in files directory to safe-to-remove folder.
      Now only the most recent package will be kept in files directory for patch creation

* Fixed

  - Install from setup.py
  - Failed password retry

* Removed

v0.11.0 - 2014/11/22
~~~~~~~~~~~~~~~~~~~~
* Added

  - PyiWrapper

    - Spec file support. Spec file will be rejected if onedir mode is specified.

* Updated

  - Client

    - Now each call to update_check returns 1 of 2 update objects. AppUpdate or LibUpdate. The updated objects are nearly identical. The AppUpdate object has a few more methods like restart & extract_restart. Now instead of calling client.download() you will use app_update.download(). Check the demos for more info.

  - PyiWrapper

    - Increased stability of wrapper to better parse args

  - CLI

    - start cli with pyiupdater-cli instead of pyi-cli


* Removed

  - CLI

    - Archiver Utility

v0.10.0 - 2014/11/16
~~~~~~~~~~~~~~~~~~~~
* Added

  - Secure downloading of manifest
  - Offline update

    - Upon successful online version manifest signature verification, the version file manifest will be written to the app data folder.

    - Calls to client.download() will check if update has already been downloaded & return True if the checksum verifies before attempting to download update.

  - Pyinstaller wrapper

    - Using the following command compiles your script and archives it ready for file diff and upload::

      $ pyiupdater app.py --app-name=APP --app-version=0.1.0

  - Deprecated Warnings

    - use client.extract() instead of client.install()
    - use client.extract_restart() instead of client.install_restart()

* Updated

  - URL sanitizing

    - Better handling of types passed to config class attributes

* Fixed

  - Archiving currently running app

    - Will now archive Mac.app apps

* Removed

  - Common util functions

    - They were added to jms-utils


v0.9.2 - 2014/10/19
~~~~~~~~~~~~~~~~~~~
* Fixed

  - Require PyInstaller 2.1.1 for PyiUpdater usage


v0.9.1 - 2014/10/19
~~~~~~~~~~~~~~~~~~~
* Added

  - Require PyInstaller 2.1.1 for PyiUpdater usage


v0.9.0 - 2014/10/18
~~~~~~~~~~~~~~~~~~~

* Added

  - Support for multiple update urls
  - Auto generated client config
  - ed25529 Update verification

    - Using instead of RSA

* Updated

  - Client updater

    - Support Mac GUI app bundles
    - Better error handling
    - Less failed application execution when updater
      has errors

    - Patcher

      - Now verifies patched update integrity
        against version file

  - Downloader

    - Https verification

      - on by default
      - Can disable in config file
      - VERIFY_SERVER_CERT

    - Dynamic block resizing

  - Archive Extraction

    - More reliable

  - Archive creator

    - Works with mac GUI apps

  - Private methods

    - Refactored to make testing easier


v0.8.1 - 2014/9/3
~~~~~~~~~~~~~~~~~

* Added

  - jms-utils

* Fixed

  - Packaging setup.py installation

* Removed

  - Unused tests

v0.8.0 - 2014/8/31
~~~~~~~~~~~~~~~~~~

* Added

  - Archive Maker utility

    - Makes zip & gzip archives with name, version
      and platform in correct format for package handler

  - Signals

    - If you want to run updater in background
      thread you can subscribe to signals for
      download progress and completion

  - CLI

    - Option to change encryption password

  - Initial py3 compat

  - More code comments if you want to get your
    hands dirty

  - Option to enable https verification

* Updated

  - Package Handler

    - Package metadata parsing is faster. Thanks
      to a new & shiny package object.

  - File Crypt

    - Uses simple encryption interface of
      simple-crypt. Pycrypto in background.

* Fixed

  - CLI

    - Initial setup didn't save settings
      to correct class attributes


  - Client

    - Parsing of version file


  - Patch creation

    - Example:

      1.9 > 1.10 was True

      1.9 > 1.10 is now False

* Removed

  - Cryptography dependency
  - License text from individual files
  - Unused imports

v0.7.2 - 2014/8/10
~~~~~~~~~~~~~~~~~~

* Fixed

  - Error on load cli

v0.7.1 - 2014/8/10
~~~~~~~~~~~~~~~~~~

* Added

  - Utils

    - Utils specific errors

  - KeyHandler

    - Error if DevDataDir not setup

* Updated

  - Client

    - Better parsing of old updates to remove

    - More error checking

    - More error reporting

    - Dynamic creation of archive format

  - Utils

    - Better parsing of dot files for removal

* Removed

  - Client

    - Some old transition code

v0.7 - 2014/8/3
~~~~~~~~~~~~~~~

* Added

  - Uploader plugin support
  - Default S3 & SCP plugins
  - Support for gzipped archives

* Updated

  - Menu option handling

* Remove

  - Upload code for s3 and scp
  - Unused config options
  - Redundant upload checks

v0.6.0 - 2014/7/27
~~~~~~~~~~~~~~~~~~

*** Renamed to PyiUpdater ***

* Removed

  - Old transition code
  - Binary support

    - only pip & src install
