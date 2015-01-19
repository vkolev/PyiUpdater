#--------------------------------------------------------------------------
# Copyright 2014 Digital Sapphire Development Team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#--------------------------------------------------------------------------


import argparse


def make_parser():
    parser = argparse.ArgumentParser(usage=u'%(prog)s')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    return parser


def make_subparser(parser):
    subparsers = parser.add_subparsers(help=u'commands', dest=u'command')
    return subparsers


def add_build_parser(subparsers):
    build_parser = subparsers.add_parser(u'build', help=u'compiles script',
                                         usage=u'%(prog)s <script> [opts]')

    # Start of args override
    # start a clean build
    build_parser.add_argument(u'--clean', help=u'Clean build. '
                              u'Bypass the cache', action="store_true")
    # This will be set to the pyi-data/new directory.
    # When we make the final compressed archive we will look
    # for an exe in that dir.
    build_parser.add_argument(u'-o', help=argparse.SUPPRESS)
    build_parser.add_argument(u'--distpath', help=argparse.SUPPRESS)

    # Will be set to .pyiupdater/spec/
    # Trying to keep root dir clean
    build_parser.add_argument(u'--specpath', help=argparse.SUPPRESS)

    # Will be set to .pyiupdater/build
    # Trying to keep root dir clean
    build_parser.add_argument(u'--workpath', help=argparse.SUPPRESS)

    # Will be set to platform name i.e. mac, win, nix, nix64, arm\
    # When archiving we will change the name to the value passed to
    # --app-name
    build_parser.add_argument(u'-n', help=argparse.SUPPRESS)
    build_parser.add_argument(u'--name', help=argparse.SUPPRESS)

    # Just capturing these argument.
    # PyiUpdater only supports onefile mode at the moment
    build_parser.add_argument(u'-D', action=u"store_true",
                              help=argparse.SUPPRESS)
    build_parser.add_argument(u'--onedir', action=u"store_true",
                              help=argparse.SUPPRESS)

    # Just capturing these argument.
    # Will be added later to pyinstaller build command
    build_parser.add_argument(u'-F', action=u"store_true",
                              help=argparse.SUPPRESS)
    build_parser.add_argument(u'--onefile', action=u"store_true",
                              help=argparse.SUPPRESS)

    # Just capturing these arguments
    build_parser.add_argument(u'-c', action=u"store_true",
                              help=argparse.SUPPRESS, dest=u'_console',
                              action=u'store_true')
    build_parser.add_argument(u'--console', action=u"store_true",
                              help=argparse.SUPPRESS)
    build_parser.add_argument(u'--nowindowed', action=u"store_true",
                              help=argparse.SUPPRESS, action=u'store_true')

    build_parser.add_argument(u'-w', action=u"store_true", dest=u'_windowed',
                              help=argparse.SUPPRESS)
    build_parser.add_argument(u'--windowed', action=u"store_true",
                              help=argparse.SUPPRESS)
    build_parser.add_argument(u'--noconsole', action=u"store_true",
                              help=argparse.SUPPRESS)

    # Potentially harmful for cygwin on windows
    # ToDo: Maybe do a check for cygwin and disable if cygwin is true
    build_parser.add_argument(u'-s', action=u"store_true",
                              help=argparse.SUPPRESS)
    build_parser.add_argument(u'--strip', action=u"store_true",
                              help=argparse.SUPPRESS)
    # End of args override

    # Used by PyiWrapper
    build_parser.add_argument(u'--app-name', dest=u"app_name", required=True)
    build_parser.add_argument(u'--app-version', dest=u"app_version",
                              required=True)
    build_parser.add_argument(u'-k', u'--keep', dest=u'keep',
                              action=u'store_true',
                              help='Won\'t delete update after archiving')


def add_clean_parser(subparsers):
    clean_parser = subparsers.add_parser(u'clean',
                                         help=u'* WARNING * removes all '
                                         u'traces of pyiupdater')
    clean_parser.add_argument(u'-y', '--yes', help=u'Confirms removal of '
                              u'pyi-data & .pyiupdater folder',
                              action='store_true')


def add_init_parser(subparsers):
    init_parser = subparsers.add_parser(u'init', help=u'initializes a '
                                        u'src directory')
    init_parser.add_argument(u'-c', u'--count', help=u'How many key pairs to '
                             u'create. The more keys the better your chances '
                             u'are of not having an app lose its ability to '
                             u'self update. Default 3',
                             type=int, default=3)


def add_keys_parser(subparsers):
    keys_parser = subparsers.add_parser(u'keys', help=u'Manage signing keys')
    keys_parser.add_argument(u'--revoke', help=u'Revokes oldest signing key & '
                             u'adds the same amount of new good key pairs to '
                             u'keys db. Verson file will no longer be signed '
                             u'by revoked keys. Default 1',
                             type=int)
    keys_parser.add_argument(u'--show-private', help=u'Prints private key to '
                             u'screen upon revocation', dest=u'private',
                             action='store_true')


def add_log_parser(subparsers):
    log_parser = subparsers.add_parser(u'log', help=u'Generate log archive to '
                                       u'help debugging. Archive will be '
                                       u'place in current working directory')
    log_parser.add_argument(u'--dummy', help=argparse.SUPPRESS)


def add_package_parser(subparsers):
    package_parser = subparsers.add_parser(u'pkg', help=u'Manages creation of '
                                           u'file metadata & signing')
    package_parser.add_argument(u'-P', u'--process',
                                help=u'Adds update metadata to version file',
                                action=u'store_true', dest=u'process')

    package_parser.add_argument(u'-S', u'--sign', help=u'Sign version file',
                                action=u'store_true', dest=u'sign')


def add_upload_parser(subparsers):
    upload_parser = subparsers.add_parser(u'upload', help=u'Uploads files')
    upload_parser.add_argument(u'-s', u'--service', help=u'Where '
                               u'updates are stored', dest=u'service')


def add_version_parser(subparsers):
    version_parser = subparsers.add_parser(u'version',
                                           help=u'Programs version')
    version_parser.add_argument(u'--dummy', help=argparse.SUPPRESS)


def get_parser():
    parser = make_parser()
    subparsers = make_subparser(parser)
    add_build_parser(subparsers)
    add_clean_parser(subparsers)
    add_init_parser(subparsers)
    add_keys_parser(subparsers)
    add_log_parser(subparsers)
    add_package_parser(subparsers)
    add_upload_parser(subparsers)
    add_version_parser(subparsers)
    return parser
