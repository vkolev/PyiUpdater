:orphan:

Welcome to PyiUpdater
=====================

What is PyiUpdater?
~~~~~~~~~~~~~~~~~~~

In its simplest form PyiUpdater is a collection of modules, when used together, makes its super simple to add auto-update functionality to your app.

A high level break down of the framework consists of 3 parts.

Client
    Is the module you import into your app that provides the update functionality.

Core
    Consists of the Archiver, Downloader, FileCrypt, KeyHandler, Patcher & Utils.

CLI
    A terminal app that provides menu driven access to meta-data grabbing, update diff's, signing & uploading of application updates. The CLI uses the core to provide this functionality.

Status
~~~~~~

Starting with v0.9.2 PyiUpdater supports updating GUI & cli apps on Mac, Windows & Linux. The api is pretty stable but maintaining backwards compatibility is on a best effort basis until v1.0 Backwards incompatible changes will be noted in the changelog.

Contents:

.. toctree::
    :maxdepth: 2

    downloads
    installation
    configuration
    usage
    architecture
    folder_structure
    api
    release_history


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`