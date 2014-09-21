.. _configuration:

Configuration
=============

.. tabularcolumns:: |p{6.5cm}|p{8.5cm}|

================================= =========================================
``APP_DATA_DIR``                  Directory where updates of app & libs are
                                  cached. Created dynamically.
``APP_NAME``                      Name of your app. Excluding the ".exe"
                                  on windows. Used to create APP_DATA_DIR
``COMPANY_NAME``                  Company or your name.  Used to create
                                  APP_DATA_DIR
``DEBUG``                         enable/disable debug mode
``DEV_DATA_DIR``                  Directory on dev machine for PyiUpdater to
                                  do its work. Defaults to Current Working Directory
``KEY_LENGTH``                    Length of Key Pair. Must be a multipule
                                  of 256. Default 2048. In 2014 you should
                                  not use a key length less then 2048.
``PRIVATE_KEY_NAME``              Name given to your private key. Defaults
                                  to APP_NAME.pem
``PUBLIC_KEY_NAME``               Name given to your public key. Defaults
                                  to APP_NAME.pub
``PUBLIC_KEY``                    Public key.  Used on client side
``UPDATE_URL``                    Where clients looks for updates
``UPDATE_PATCHES``                enable/disable creation of patches
``REMOTE_DIR``                    Remote directory/Bucket Name
``HOST``                          Remote host to connect to for ssh
``USERNAME``                      Username/API Key
``PASSWORD``                      Password/API Secret
``SSH_KEY_PATH``                  Path to ssh private key
================================= =========================================