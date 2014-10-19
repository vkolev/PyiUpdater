.. _installation:

Installation
============

PyiUpdater depends on a few external libraries: `boto <http://aws.amazon.com/sdkforpython/>`_,  `bsdiff4 <https://github.com/ilanschnell/bsdiff4>`_, `cryptography <https://cryptography.io/en/latest/>`_, `paramiko <https://github.com/paramiko/paramiko>`_, `pbkdf2 <http://www.dlitz.net/software/python-pbkdf2/>`_ , `pycrypto <https://www.dlitz.net/software/pycrypto/>`_ & `scp <https://github.com/jbardin/scp.py>`_. Bsdiff4 is only required to make patches, not to apply them.  These libraries are not documented here.

So how do you get all that on your computer quickly?

Install from pip::

    $ pip install PyiUpdater

S3 & SCP uploaders are available with::

    $ pip install PyiUpdater[s3]

    $ pip install PyiUpdater[scp]

If you want the bleeding edge download a pre-release version. WARNING - pre released version may not work as expected::

    $ pip install PyiUpdater --pre