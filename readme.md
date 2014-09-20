[![PyPI version](https://badge.fury.io/py/PyiUpdater.svg)](http://badge.fury.io/py/PyiUpdater) [![Build Status](https://travis-ci.org/JohnyMoSwag/PyiUpdater.svg?branch=master)](https://travis-ci.org/JohnyMoSwag/PyiUpdater) [![Coverage Status](https://coveralls.io/repos/JohnyMoSwag/PyiUpdater/badge.png?branch=master)](https://coveralls.io/r/JohnyMoSwag/PyiUpdater?branch=master)

# PyiUpdater
##### This framework does most of the heavy lifting regarding updating your app or library.  PyiUpdater will scan your update archive, grab meta-data from filename, get checksums, make patches, get patch checksums, update version file, sign version file with private key, backs up packages to files folder then moves all packages to deploy folder ready for upload.  All from the cli or programmatically.  PyiUpdater also handles the creation of your public and private keys.  Keys are used for update manifest verification. PyiUpdater also includes a client module you can import into your app to check for updates, download, install & restart your app. The client module also cleans up old updates on the end users computer.

######[Change Log](https://github.com/JohnyMoSwag/PyiUpdater/blob/master/changelog.txt "Change Log")

## To Install

#### From pip:

    $ pip install PyiUpdater

#### From source:

    $ python setup.py install

## Usage:

#### Start guided setup with pip or setup.py install

    $ pyi-cli

#### Start guided setup without installation

    $ python start_cli.py

#### Archive maker utility usage
The filename for an update must include mac, win, arm, nix or nix64. For example, FILE1 could be myapp-mac & FILE2 mylib-nix.

    $ pyi-archiver -h
    Usage: pyi-archive -n "My App" -v 1.0.1 FILE [FILE...]
    Usage: pyi-archive -i gzip -n "My App" -v 1.0.1 FILE [FILE...]

    Options:
      -h, --help            show this help message and exit
      -c ARCHIVER, --archiver=ARCHIVER
                            Type of archive compression to use
      -n NAME, --name=NAME  Name of update
      -v VERSION, --version=VERSION
                            Version # of update. Must have Major.Minor.Patch even if it's 0 eg. 1.1.0
      --keep                Do not delete source file

#### Can also be used programmatically
######[Click Here To See Example Dev Script](https://github.com/JohnyMoSwag/PyiUpdater/blob/master/examples/programtically.py "Example Usage")


#### How to use client to update your app or a libary your app depends on:

    # You can update your apps and libs or binaries you app relies on.
    from threading import Thread
    from blinker import Signal

    from pyi_updater import Client

    class ClientConfig(object):
        APP_NAME = 'App name'
        COMPANY_NAME = 'Your name or company'
        PUBLIC_KEY = (26810719857825024839344902213073312263506443291817742739127949147323743659423081696962181574485073366946821823656546710698255775467708598618269670406584294193972684367702826926688139841968731194015789180684686551768298110771590605237915611408133047956218865434660274610222609095554041517443565839110764395166743158953027083690492927575231987598020768390433860118087169346203942443062194554114528508192560088005644912398573361844543757472527724779977152153381024599977904605796890617980849686972801453252752148799208320716467436186778883537406884501769657736396569192751657230762919699367606205570509492855308457559271L, 65537)
        UPDATE_URL = 'https://s3-us-west-1.amazonaws.com/PyiUpdater/'

    client = Client(ClientConfig())
    # Install and restart with one method call
    # install_restart() and restart() will fail if update is not
    # an executable.
    # If updating a lib just use install and take over from there
    updates_available = client.update_check('7-zip', '0.0.1')

    # Example of download on a background thread with
    # a callback
    progress_signal = Signal('progress_info')

    progress_signal.connect
    def install_restart(sender, **kw):
        # Here you could as the user here if they would
        # like to install the new update and restart
        if sender.name == 'progress_info':
            if 'Successful' in kw['info']:
                client.install_restart()

    t = Thread(target=client.download)
    t.start()

    # Example of downloading on the main thread
    if update_available:
        downloaded = client.download()
        if downloaded:
            client.install_restart()

    # Install then restart later
    success = client.update_check('gist', '11.0.1')
    if success:
        client.install()

    answer = raw_input('Would you like to install update now?')
    if 'y' in answer:
        client.restart()

    # Lastly to just download an update or lib and extract to update folder
    updates_availabe = client.update_check('libfoo', '1.2.3')
    if updates_available:
        client.install()

## Write your own upload plugin
###### Use pyiu.uploaders for your plugin namespace
[Plugin wiki](https://github.com/JohnyMoSwag/PyiUpdater/wiki/Make-an-upload-plugin "Plugin wiki")

#### Examples available
###### [S3 Plugin](https://github.com/JohnyMoSwag/pyiupdater-s3-plugin "S3 Plugin")
###### [SCP Plugin](https://github.com/JohnyMoSwag/pyiupdater-scp-plugin "SCP Plugin")

## Support Archive Formats
###### Only zip and gzipped for now.  Constraints being on patch size.

#### Archive Patch Tests:
Format  -  Source  -  Dest  -  Patch

7z - 6.5mb - 6.8mb -  6.8mb

bz2 - 6.6mb - 6.8mb - 6.9mb

zip - 6.5mb - 6.8mb - 3.2mb

gz - 6.5mb - 6.8mb - 3.2mb
