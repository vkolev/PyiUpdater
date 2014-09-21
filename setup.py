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
    url='pyiupdater.johnymoswag.com',
    download_url=('https://github.com/JohnyMoSwag/Pyi'
                  'Updater/archive/master.zip'),
    license='Apache License 2.0',
    dependency_links=['https://github.com/pyinstaller/pyinstaller/archive/de'
                      'velop.zip#egg=pyinstaller-2.1.1'],
    extras_require = {
        'scp': 'PyiUpdater-scp-Plugin',
        },
    install_requires=[
        'appdirs',
        'blinker',
        'bsdiff4',
        'jms-utils',
        'pycrypto',
        'pyinstaller',
        'PyiUpdater-s3-Plugin',
        'requests',
        'six',
        'simple-crypt',
        'stevedore',
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
