.. _installation:

Installation
============

PyiUpdater depends on a few external libraries: `appdirs <https://pypi.python.org/pypi/appdirs/>`_, `blinker <https://pypi.python.org/pypi/blinker>`_, `boto <http://aws.amazon.com/sdkforpython/>`_,  `bsdiff4 <https://github.com/ilanschnell/bsdiff4>`_, `certifi <https://pypi.python.org/pypi/certifi>`_, `ed25519 <https://pypi.python.org/pypi/ed25519>`_, `jms_utils <https://pypi.python.org/pypi/JMS-Utils>`_ , `pyinstaller <https://github.com/pyinstaller/pyinstaller>`_, `simple_pbkdf2 <https://pypi.python.org/pypi/simple-pbkdf2>`_, `six <https://pypi.python.org/pypi/six>`_, `stevedore <https://pypi.python.org/pypi/stevedore>`_ & `urllib3 <https://pypi.python.org/pypi/urllib3>`_. Bsdiff4 is only required to make patches, not to apply them.  These libraries are not documented here.

So how do you get all that on your computer quickly?

Install from pip::

    $ pip install PyiUpdater --process-dependency-links

S3 & SCP upload plugins are available with::

    $ pip install PyiUpdater[s3] --process-dependency-links

    $ pip install PyiUpdater[scp] --process-dependency-links

If you want the bleeding edge download a pre-release version. WARNING! -> pre released version may not work as expected::

    $ pip install PyiUpdater --pre --process-dependency-links