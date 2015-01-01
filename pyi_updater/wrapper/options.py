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


parser = argparse.ArgumentParser(usage=u'%(prog)s')
subparsers = parser.add_subparsers(help=u'commands', dest=u'command')

build_parser = subparsers.add_parser(u'build', help=u'compiles script',
                                     usage=u'%(prog)s <script> [opts]')
# Start of args override
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
# ToDo: Take a closer look at this switch
build_parser.add_argument(u'-c', action=u"store_true",
                          help=argparse.SUPPRESS)
build_parser.add_argument(u'--console', action=u"store_true",
                          help=argparse.SUPPRESS)
build_parser.add_argument(u'--nowindowed', action=u"store_true",
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
build_parser.add_argument(u'--app-version', dest=u"app_version", required=True)
build_parser.add_argument(u'-k', u'--keep', dest=u'keep', action=u'store_true',
                          help='Won\'t delete update after archiving')


init_parser = subparsers.add_parser(u'init', help=u'initializes a '
                                    u'src directory')

keys_parser = subparsers.add_parser(u'keys', help=u'Manage signing keys: '
                                    u'Not Implemented')


package_parser = subparsers.add_parser(u'pkg', help=u'Manages creation of '
                                       u'file metadata & signing')
package_parser.add_argument(u'-p', u'--process',
                            help=u'Adds update metadata to version file',
                            action=u'store_true', dest=u'process')

package_parser.add_argument(u'-s', u'--sign', help=u'Sign version file',
                            action=u'store_true', dest=u'sign')

upload_parser = subparsers.add_parser(u'up', help=u'Uploads files')
upload_parser.add_argument(u'-s', u'--service', help=u'Where '
                           u'updates are stored', dest=u'service')

version_parser = subparsers.add_parser(u'version', help=u'Programs version')
