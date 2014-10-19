v0.10.0 - master
~~~~~~~~~~~~~~~~
.. note:: This version is not yet released and is under active development.


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
