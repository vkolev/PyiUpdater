## Demos
So if you opt not to use the cli interface & instead want to integrate PyiUpdater into your build, check out the dev_machine.py demo.

PyiUpdater make heavy use of the pyi-data folder.

####Steps

######1. Have your configuration file set
| ConfigClass Attribute | Description |
| --------------------- | ----------- |
|APP_NAME         | (str) Name of your app. Used with COMPANY_NAME to create an update cache dir on end user system.|
|COMPANY_NAME     | (str) Company or your name.  Used with APP_NAME to create an update cache dir on end user system.|
|DEV_DATA_DIR     | (str) Full path to directory where pyiupdater will keep work files. i.e signing keys, src file for patch creation, etc.|
|PUBLIC_KEY       | (tuple) Used on client side for authentication |
|UPDATE_URL       | (str) Where clients search for updates - * Deprecated! You can put a single url in the list of UPDATE_URLS *|
|UPDATE_URLS       | (list) A list of url(s) where a client will look for needed update objects. |
|UPDATE_PATCHES   | (bool) enable/disable creation of patch updates |
|REMOTE_DIR       | (str) Remote directory/Bucket name to place update files |
|HOST             | (str) Remote host to connect to for server uploads |
|USERNAME         | (str) Username/API Key for uploading updates |
|PASSWORD         | (str) Password/API Secret/Path to ssh private key for uploading updates |

######2. Build your app:

    $ pyiupdater app.py --app-name=APP --app-version=0.1.0


######3. Use PackageHandler's process_packages method. Will move copy app updates to version folder in the files dir & also move udpate form new folder to deploy folder

######4. Now use KeyHanlder sign_update method to add a signature to the version file & copies it to the deploy dir.
