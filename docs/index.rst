:orphan:

Welcome to PyiUpdater
=====================

PyiUpdater - Update Framework!

This framework does most of the heavy lifting regarding updating your app
or library.  PyiUpdater will scan your update archive, grab meta-data from filename, get checksums, make patches, get patch checksums, update version file, sign version file with private key, backs up packages to files folder
then moves all packages to deploy folder ready for upload.  All from the
cli or programmatically.  PyiUpdater also handles the creation of your public
and private keys.  Keys are used for update manifest verification. PyiUpdater also includes a client module you can import into your app to check for updates, download, install & restart your app. The client module also cleans up old updates on the end users computer.

Contents:

.. toctree::
    :maxdepth: 2

    downloads
    installation
    configuration
    usage
    folder_structure
    api
    release_history


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`