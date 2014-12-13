#!/usr/bin/env python

try:
    from setuptools import Command, find_packages, setup
except ImportError:
    from distutils.core import Command, find_packages, setup
import subprocess
import sys


sys.path.insert(0, 'src')

from pyi_updater.version import get_version


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        errno = subprocess.call([sys.executable, 'runtests.py'])
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
        's3': 'PyiUpdater-s3-Plugin>=0.11',
        'scp': 'PyiUpdater-scp-Plugin>=0.9',
        },
    cmdclass = {'test': PyTest},
    install_requires=[
        'appdirs',
        'blinker',
        'bsdiff4',
        'certifi',
        'cryptography',
        'ed25519',
        'jms-utils >= 0.4.6',
        'pyinstaller >= 2.1.1dev',
        'simple-pbkdf2',
        'six',
        'stevedore',
        'urllib3',
        ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points="""
    [console_scripts]
    pyiupdater=pyi_updater.pyiwrapper:main
    pyiupdater-cli=cli_ui:main
    pyi-cli=cli_ui:main
    """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7'],
    )
