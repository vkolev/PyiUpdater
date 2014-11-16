[![PyPI version](https://badge.fury.io/py/PyiUpdater.svg)](http://badge.fury.io/py/PyiUpdater) [![Build Status](https://travis-ci.org/JohnyMoSwag/PyiUpdater.svg?branch=master)](https://travis-ci.org/JohnyMoSwag/PyiUpdater) [![Coverage Status](https://coveralls.io/repos/JohnyMoSwag/PyiUpdater/badge.png?branch=master)](https://coveralls.io/r/JohnyMoSwag/PyiUpdater?branch=master)

# PyiUpdater
##### An update framework for managing, signing & uploading your app updates
[Documentation](http://pyiupdater.jmsapps.net)

[Dev Documentation](http://pyiupdater-dev.jmsapps.net)


[Full changelog](https://github.com/JohnyMoSwag/PyiUpdater/blob/master/changelog.txt)

#### Supported Freezers
* [Pyinstaller](http://www.pyinstaller.org) >= 2.1.1


## To Install

#### Stable:

    $ pip install PyiUpdater --process-dependency-links

#### Dev:

    $ pip install PyiUpdater --pre --process-dependency-links

###### S3 & SCP uploaders are available with

    $ pip install PyiUpdater[s3] --process-dependency-links

or

    $ pip install PyiUpdater[scp] --process-dependency-links


## Usage:

#### Start guided setup with pip or setup.py install

    $ pyi-cli

#### Can also be used programmatically
######[Click Here To See Example Work Flow](https://github.com/JohnyMoSwag/PyiUpdater/tree/master/examples "Example Usage")


## Write your own upload plugin
###### Use pyiu.uploaders for your plugin namespace
[Plugin wiki](https://github.com/JohnyMoSwag/PyiUpdater/wiki/Make-an-upload-plugin "Plugin wiki")

#### Examples available
###### [S3 Plugin](https://github.com/JohnyMoSwag/pyiupdater-s3-plugin "S3 Plugin")
###### [SCP Plugin](https://github.com/JohnyMoSwag/pyiupdater-scp-plugin "SCP Plugin")

## Support Archive Formats
###### Only zip and gzipped for now.  Constraints being on patch size.

#### Archive maker utility usage
The filename for an update must include system version in form of mac, win, arm, nix or nix64. For example, FILE1 could be myapp-mac & FILE2 could be mylib-nix.

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

#### Archive Patch Tests:
Format  -  Src  -  Dst  -  Patch

7z - 6.5mb - 6.8mb -  6.8mb

bz2 - 6.6mb - 6.8mb - 6.9mb

zip - 6.5mb - 6.8mb - 3.2mb

gz - 6.5mb - 6.8mb - 3.2mb
