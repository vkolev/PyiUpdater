## Demos
So if you opt not to use the cli interface & instead want to integrate PyiUpdater into your build, check out the progmatically.py demo.

PyiUpdater make heavy use of the pyi-data folder.

Steps

1. Build your app and place in new folder

2. User pyi-archiver -n "Your app name" -v 1.0.0 "Full path of app in new folder". Make sure win, mac, arm, nix or nix64 in somewhere in the filename.
The archiver uses this for selecting the correct archive format and naming
the final archive.

3. Use PackageHandler process_packages method. Will move copy app updates to version folder in the files dir & also move udpate form new folder to deploy folder

4. Now use KeyHanlder sign_update method to add a signature to the version file & copies it to the deploy dir.


#### Config Options
| ConfigClass Attribute | Description |
| --------------------- | ----------- |
|APP_NAME         | Name of your app. Used with COMPANY_NAME to create an update cache dir on end user system.|
|COMPANY_NAME     | Company or your name.  Used with APP_NAME to create an update cache dir on end user system.|
|PUBLIC_KEY       | Used on client side for authentication |
|UPDATE_URL       | Where clients search for updates - * Deprecated! You can put a single url in the list of UPDATE_URLS *|
|UPDATE_URLS       | A list of url(s) where a client will look for needed update objects. |
|UPDATE_PATCHES   | enable/disable creation of patch updates |
|REMOTE_DIR       | Remote directory/Bucket name to place update files |
|HOST             | Remote host to connect to for server uploads |
|USERNAME         | Username/API Key for uploading updates |
|PASSWORD         | Password/API Secret/Path to ssh private key for uploading updates |
