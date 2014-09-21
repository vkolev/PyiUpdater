.. _installation:

Installation
============

PyiUpdater depends on a few external libraries: `boto <http://aws.amazon.com/sdkforpython/>`_,  `bsdiff4 <https://github.com/ilanschnell/bsdiff4>`_, `cryptography <https://cryptography.io/en/latest/>`_, `paramiko <https://github.com/paramiko/paramiko>`_, `pbkdf2 <http://www.dlitz.net/software/python-pbkdf2/>`_ , `pycrypto <https://www.dlitz.net/software/pycrypto/>`_ & `scp <https://github.com/jbardin/scp.py>`_. Bsdiff4 is only required to make patches, not to apply them.  These libraries are not documented here.

So how do you get all that on your computer quickly?

Install from pip::

    home$ pip install PyiUpdater

Install from source::

    home$ python setup.py install

Pip will be the easiest way to install & upgrade to the latest stable
version of this framework. If you want the bleeding edge download from github `dev branch <https://github.com/JohnyMoSwag/PyiUpdater/archive/dev.zip>`_. You will need Python 2.7 to get started, so be sure to have an up-to-date Python 2.7 installation.