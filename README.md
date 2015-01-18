[![Downloads](https://pypip.in/download/PyiUpdater/badge.svg)](https://pypi.python.org/pypi/PyiUpdater/)
[![Development Status](https://pypip.in/status/PyiUpdater/badge.svg)](https://pypi.python.org/pypi/PyiUpdater/)
[![Coverage Status](https://coveralls.io/repos/JohnyMoSwag/PyiUpdater/badge.svg?branch=master)](https://coveralls.io/r/JohnyMoSwag/PyiUpdater?branch=master)
[![Circle CI](https://circleci.com/gh/JohnyMoSwag/PyiUpdater.svg?style=svg)](https://circleci.com/gh/JohnyMoSwag/PyiUpdater)

# PyiUpdater
##### An update framework for managing, signing & uploading your app updates
[Documentation](http://pyiupdater.jmswag.com)

[Dev Documentation](http://pyiupdater-dev.jmswag.com)


[Full changelog](https://github.com/JohnyMoSwag/PyiUpdater/blob/master/changelog.txt)

#### Supported Freezers
* [Pyinstaller](http://www.pyinstaller.org) >= 2.1


## To Install

#### Stable:

    $ pip install PyiUpdater

#### Dev:

    $ pip install PyiUpdater --pre

#### Extras:
######S3 & SCP upload plugins are available with

    $ pip install PyiUpdater[s3]

or

    $ pip install PyiUpdater[scp]


## Usage:

#### To compile & package your script

    $ pyiupdater build app.py --app-name=APP --app-version=0.1.0


#### For creating update diff's, updating your version file & uploading your update

    $ pyiupdater pkg --process

    $ pyiupdater pkg --sign

#### Upload your updates to Amazon S3

    $ pyiupdater up --service s3


###### Using programmatically
######[Click Here To See Example Work Flow](https://github.com/JohnyMoSwag/PyiUpdater/tree/master/demos "Example Usage")


## Write your own upload plugin
###### Use pyiu.uploaders for your plugin namespace
[Plugin wiki](https://github.com/JohnyMoSwag/PyiUpdater/wiki/Make-an-upload-plugin "Plugin wiki")

#### Examples available
###### [S3 Plugin](https://github.com/JohnyMoSwag/pyiupdater-s3-plugin "S3 Plugin")
###### [SCP Plugin](https://github.com/JohnyMoSwag/pyiupdater-scp-plugin "SCP Plugin")

## Support Archive Formats
###### Zip for Windows and GZip for Mac & Linux.  Constraints being on patch size.

#### Archive Patch Tests:
Format  -  Src  -  Dst  -  Patch

7z - 6.5mb - 6.8mb -  6.8mb

bz2 - 6.6mb - 6.8mb - 6.9mb

zip - 6.5mb - 6.8mb - 3.2mb

gz - 6.5mb - 6.8mb - 3.2mb
