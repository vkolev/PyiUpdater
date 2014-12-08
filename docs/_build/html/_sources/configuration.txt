.. _configuration:

Configuration
=============

.. tabularcolumns:: |p{6.5cm}|p{8.5cm}|

================================= =========================================
``APP_NAME``                      (str) Name of your app. Used with
                                  COMPANY_NAME to create an update cache dir on end user system.
``COMPANY_NAME``                  (str) Company or your name.  Used with
                                  APP_NAME to create an update cache dir on end user system.
``DEV_DATA_DIR``                  (str) Full path to directory where
                                  pyiupdater will keep work files. i.e signing
                                  keys, src file for patch creation, etc.
``PUBLIC_KEY``                    (tuple) Used on client side for
                                  authentication
``UPDATE_URL``                    (str) Where clients search for updates
                                  - * Deprecated! You can put a single url
                                  in the list of UPDATE_URLS *
``UPDATE_URLS``                   (list) A list of url(s) where a client will
                                  look for needed update objects.
``UPDATE_PATCHES``                (bool) Enable/disable creation of patch
                                  updates
``REMOTE_DIR``                    (str) Remote directory/Bucket name to place
                                  update files
``HOST``                          (str) Remote host to connect to for server
                                  uploads
``USERNAME``                      (str) Username/API Key for uploading updates
``PASSWORD``                      (str) Password/API Secret/Path to ssh private
                                  key or uploading updates
================================= =========================================