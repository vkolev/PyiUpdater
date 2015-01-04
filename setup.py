#!/usr/bin/env python

from setuptools import Command, find_packages, setup
import subprocess
import sys

import versioneer

from pyi_updater.version import get_version

versioneer.VCS = 'git'
versioneer.versionfile_source = 'pyi_updater/_version.py'
versioneer.versionfile_build = 'pyi_updater/_version.py'
versioneer.tag_prefix = ''  # tags are like 1.2.0
versioneer.parentdir_prefix = 'PyiUpdater-'  # dirname like 'myproject-1.2.0'


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        errno = subprocess.call([sys.executable, u'runtests.py', u'-v'])
        raise SystemExit(errno)


class PyTestCover(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        errno = subprocess.call([sys.executable, u'runtests.py', u'tests',
                                u'--cov', u'pyi_updater', u'-n', u'1'])
        raise SystemExit(errno)

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
    dependency_links = [
        'https://github.com/pyinstaller/pyinstaller/tarball/'
        'develop#egg=pyinstaller-2.1.1dev'],
    extras_require = {
        's3': 'PyiUpdater-s3-Plugin>=1.0.1',
        'scp': 'PyiUpdater-scp-Plugin>=1.0',
        },
    tests_require = ['pytest', ],
    cmdclass = {'test': PyTest,
                'ctest': PyTestCover,
                'versioneer': versioneer.get_cmdclass()
                },
    install_requires=[
        'appdirs',
        'blinker',
        'bsdiff4',
        'certifi',
        # Will try to implement later
        # 'click',
        'ed25519',
        'jms-utils >= 0.5.2',
        'pyinstaller >= 2.1.1dev',
        'simple-pbkdf2',
        'six',
        'stevedore',
        'urllib3',
        ],
    packages=find_packages(),
    entry_points="""
    [console_scripts]
    pyiupdater=pyi_updater.wrapper:main
    """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7'],
    )
