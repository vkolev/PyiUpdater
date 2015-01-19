.. _usage:

Usage
~~~~~

After compiling your program with pyinstaller or any freezer that compiles python into a single executable.

Use the Archiver Maker for easy update compression & naming.

Version numbers are in the form of: x.x.x

Check `Semantic Versioning <http://semver.org/>`_ for more info

The easiest way to get started quickly is to use to command line tool. After setup is complete you'll be ready to start creating updates.

All commands must be ran from root or repository.
-------------------------------------------------

Initialize a new repository.

::

    $ pyiupdater init


To create your first update.
::

    $ pyiupdater --app-name"Your app name" --app-version1.0.0 app.py


Get update meta data and save to file.
::

    $ pyiupdater pkg -P


Sign update file with signing keys & gzip compress.
::

    $ pyiupdater pkg -S


Upload to remote location.
::

    $ pyiupdater up --service s3

Here using Amazon S3. Must have PYIUPDATER_PASS env set. Install with pyiupdater[s3].
::

    $ pip install pyiupdater[s3]


Demos
=====
So if you opt not to use the cli interface & instead want to integrate PyiUpdater into your build, look below.

.. literalinclude:: ../demos/dev_machine.py
    :linenos:


Limitations
===========

* Doesn't support onedir mode