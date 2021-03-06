#!/usr/bin/env python

from setuptools import setup, find_packages
import sys

sys.path.insert(0, 'src')

from pyi_updater import get_version

setup(
    name='PyiUpdater',
    version=get_version(),
    description='Simple App update framwork',
    author='Johny Mo Swag',
    author_email='johnymoswag@gmail.com',
    url='pyiupdater.jmsapps.net',
    download_url=('https://github.com/JohnyMoSwag/Pyi'
                  'Updater/archive/master.zip'),
    license='Apache License 2.0',
    extras_require = {
        's3': 'PyiUpdater-s3-Plugin>=0.11',
        'scp': 'PyiUpdater-scp-Plugin>=0.9',
        },
    install_requires=[
        'appdirs',
        'blinker',
        'bsdiff4',
        'certifi',
        'cryptography',
        'ed25519',
        'jms-utils >= 0.3.2',
        'six',
        'simple-pbkdf2',
        'stevedore',
        'urllib3',
        ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    # py_modules=['archiver'],
    entry_points="""
    [console_scripts]
    pyi-cli=cli:main
    pyi-archiver = pyi_updater.archiver:main
    """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7'],
    )
