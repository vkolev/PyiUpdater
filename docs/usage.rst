.. _usage:

Usage
=====

After compiling your program with pyinstaller or any freezer that compiles python into a single executable.

Use the Archiver Maker for easy update compression & naming.

Version numbers are in the form of: x.x.x

Check `Semantic Versioning <http://semver.org/>`_ for more info

The easiest way to get started quickly is to use to command line tool.

From Pip::

    $ pyi-cli

Initial Setup
-------------
You'll first be greeted with a Setup Assistant.

What you should see::

    *******************************************************
                PyiUpdater v0.7 - Setup Assistant
    *******************************************************


                                Let's begin...

    Please enter app name - No Default Available
    -->


After you enter all required information you can password protect
you config with a password. It's very import to remember this password.

What you should see::

    Enter password
    -->

    Enter passoword again
    -->

    Enter password


After setup is complete you'll be greeted with the screen below::

    *******************************************************
                    PyiUpdater v0.7 - Main Menu
    *******************************************************

    1. Sign Updates
    2. Upload
    3. Keys
    4. Settings
    5. Quit


Archive maker utility usage
---------------------------
The filename for an update must include mac, win, arm, nix or nix64. For example, FILE1 could be myapp-mac & FILE2 mylib-nix::

    $ pyi-archiver -h
    Usage: pyi-archive -n "My App" -v 1.0.1 FILE1 FILE2
    Usage: pyi-archive -i gzip -n "My App" -v 1.0.1 FILE1 FILE2

    Options:
      -h, --help            show this help message and exit
      -c ARCHIVER, --archiver=ARCHIVER
                            Type of archive compression to use
      -n NAME, --name=NAME  Name of update
      -v VERSION, --version=VERSION
                            Version # of update. Must have Major.Minor.Patch even if it's 0 eg. 1.1.0
      --keep                Do not delete source file


Check out the examples folder to see how to use the framework programmatically, to easily PyiUpdater into your existing setup.

The cli tool uses the framework almost exactly the same as the dev script but is easier for beginners. A guided setup example is also provided.

Example updater
---------------

.. literalinclude:: ../examples/client_update.py
   :linenos: