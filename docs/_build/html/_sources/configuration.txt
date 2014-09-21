.. _configuration:

Configuration
=============

.. tabularcolumns:: |p{6.5cm}|p{8.5cm}|

================================= =========================================
``APP_NAME``                      Name of your app. Used with COMPANY_NAME
                                  to create an update cache dir on end user
                                  system.
``COMPANY_NAME``                  Company or your name.  Used with APP_NAME
                                  to create an update cache dir on end user
                                  system.
``KEY_LENGTH``                    Length of Key Pair. Must be a multiple of
                                  256. Default 2048. In 2014 you should not
                                  use a key length less then 2048.
``PUBLIC_KEY``                    Used on client side for authentication
``UPDATE_URL``                    Where clients search for updates
``UPDATE_PATCHES``                nable/disable creation of patch updates
``REMOTE_DIR``                    Remote directory/Bucket name to place
                                  update files
``HOST``                          Remote host to connect to for server
                                  uploads
``USERNAME``                      Username/API Key for uploading updates
``PASSWORD``                      Password/API Secret/Path to ssh private
                                  key or uploading updates
================================= =========================================