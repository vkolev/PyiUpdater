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
                PyiUpdater v0.9 - Setup Assistant
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
                    PyiUpdater v0.9 - Main Menu
    *******************************************************

    1. Sign Updates
    2. Upload
    3. Keys
    4. Settings
    5. Quit


Demos
-----
So if you opt not to use the cli interface & instead want to integrate PyiUpdater into your build, check out the progmatically.py demo.

PyiUpdater make heavy use of the pyi-data folder.

Steps

1. Build your app and place in new folder

2. Use pyi-archiver to archive you files

3. Use PackageHandler process_packages method. Will move copy app updates to version folder in the files dir & also move udpate form new folder to deploy folder

4. Now use KeyHanlder sign_update method to add a signature to the version file & copies it to the deploy dir.