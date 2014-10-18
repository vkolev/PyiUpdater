## Demos
So if you opt not to use the cli interface & instead want to integrate PyiUpdater into your build check out the progmatically.py demo.

PyiUpdater functions around the pyi-data folder.
In your build system after you make your app your want to place it
in the new folder.


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
