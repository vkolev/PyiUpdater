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
import logging
import os
import re
import subprocess
import sys
import time

from jms_utils.logger import log_format_string
from jms_utils.paths import app_cwd, ChDir
from jms_utils.system import get_system
import stevedore

log = logging.getLogger()
log.setLevel(logging.DEBUG)
fmt_str = log_format_string()
nh = logging.NullHandler()
nh.setLevel(logging.DEBUG)
log.addHandler(nh)

from pyi_updater import PyiUpdater
from pyi_updater.config import Loader, SetupConfig
from pyi_updater.exceptions import UploaderError
from pyi_updater.utils import initial_setup, make_archive
from pyi_updater.version import get_version

if os.path.exists(os.path.join(app_cwd, u'pyi.log')):
    ch = logging.FileHandler(os.path.join(app_cwd, u'pyi.log'))
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(log_format_string())
    log.addHandler(ch)

start = time.time()
CWD = os.getcwd()
loader = Loader()

parser = argparse.ArgumentParser(usage=u'%(prog)s')

subparsers = parser.add_subparsers(help=u'commands', dest=u'command')

build_parser = subparsers.add_parser(u'build', help=u'compiles script',
                                     usage=u'%(prog)s <script> [opts]')

init_parser = subparsers.add_parser(u'init', help=u'initializes a '
                                    u'src directory')

keys_parser = subparsers.add_parser(u'keys', help=u'Manage signing keys: '
                                    u'Not Implemented')


package_parser = subparsers.add_parser(u'pkg', help=u'Manages creation of '
                                       u'file metadata & signing')

upload_parser = subparsers.add_parser(u'up', help=u'Uploads files')


version_parser = subparsers.add_parser(u'version', help=u'Programs version')


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


package_parser.add_argument(u'-p', u'--process',
                            help=u'Adds update metadata to version file',
                            action=u'store_true', dest=u'process')

package_parser.add_argument(u'-s', u'--sign', help=u'Sign version file',
                            action=u'store_true', dest=u'sign')

upload_parser.add_argument(u'-s', u'--service', help=u'Where '
                           u'updates are stored', dest=u'service')


def check_repo():
    if not os.path.exists(u'.pyiupdater'):
        sys.exit('Not a PyiUpdater repo: Must init first.')


def main():
    args = sys.argv[1:]
    args, pyi_args = parser.parse_known_args(args)
    cmd = args.command
    if cmd == u'build':
        builder(args, pyi_args)
    elif cmd == u'init':
        setup()
    elif cmd == u'up':
        upload(args)
    elif cmd == u'pkg':
        process(args)
    elif cmd == u'version':
        print(u'PyiUpdater {}'.format(get_version()))
    else:
        sys.exit(u'Not Implemented')


def process(args):
    check_repo()
    pyiu = PyiUpdater(loader.load_config())
    if args.process is False and args.sign is False:
        sys.exit(u'You must specify a command')

    if args.process is True:
        print(u'Processing packages...\n')
        pyiu.process_packages()
        print(u'Processing packages complete\n')
    if args.sign is True:
        print(u'Signing packages...\n')
        pyiu.sign_update()
        print(u'Signing packages complete\n')


def setup():
    if not os.path.exists(os.path.join(u'.pyiupdater', u'config.data')):
        config = initial_setup(SetupConfig())
        print(u'\nCreating pyi-data dir...\n')
        pyiu = PyiUpdater(config)
        pyiu.setup()
        print(u'\nMaking signing keys...')
        pyiu.make_keys()
        config.PUBLIC_KEY = pyiu.get_public_key()
        loader.save_config(config)
        print(u'\nSetup complete')
    else:
        sys.exit(u'Not an empty PyiUpdater repository')


def upload(args):
    check_repo()
    upload_service = args.service
    if upload_service is None:
        sys.exit('Must provide service name')
    password = os.environ.get('PYIUPDATER_PASS')
    if password is None:
        sys.exit('You need to set PYIUPDATER_PASS env var')
    pyiu = PyiUpdater(loader.load_config())

    class Pass(object):
        PASSWORD = password

    pyiu.update_config(Pass())

    try:
        pyiu.set_uploader(upload_service)
    except UploaderError:
        mgr = stevedore.ExtensionManager(u'pyiupdater.plugins.uploaders')
        plugin_names = mgr.names()
        log.debug(u'Plugin names: {}'.format(plugin_names))
        sys.exit(u'Invalid Uploader\n\nAvailable options:\n'
                 u'{}'.format(plugin_names))
    try:
        pyiu.upload()
    except Exception as e:
        msg = (u'Looks like you forgot to add USERNAME '
               'and/or REMOTE_DIR')
        log.debug(str(e), exc_info=True)
        sys.exit(msg)


def builder(args, pyi_args):
    check_repo()
    pyi_dir = os.path.join(os.getcwd(), u'pyi-data')
    new_dir = os.path.join(pyi_dir, u'new')
    build_dir = os.path.join(os.getcwd(), u'.pyiupdater')
    spec_dir = os.path.join(build_dir, u'spec')
    work_dir = os.path.join(build_dir, u'work')
    for d in [build_dir, spec_dir, work_dir]:
        if not os.path.exists(d):
            os.mkdir(d)

    if not os.path.exists(pyi_dir):
        sys.exit(u'pyi-data folder not found')
    if not os.path.exists(new_dir):
        sys.exit(u'pyi-data/new folder not found')

    if check_version(args.app_version) is False:
        sys.exit(u"""Error: version # needs to be in the form of "0.10.0"

    Visit url for more info:

        http://semver.org/
                  """)

    app_type = None
    for p in pyi_args:
        if p.endswith(u'.py'):
            app_type = u'script'
            break
        elif p.endswith(u'.spec'):
            spec_file = p
            app_type = u'spec'
            break
    else:
        sys.exit(u'Must pass a python script or spec file')

    if app_type == u'spec':
        fix = u"\t\t\t\t\tname='{}',".format(get_system())

        # Sanitizing spec file
        with open(spec_file, u'r') as f:
            spec_data = f.readlines()

        new_spec = []
        for s in spec_data:
            # Will replace name with system arch
            # Used for later archiving
            if u'name=' in s:
                new_spec.append(fix)
            elif u'coll' in s or u'COLLECT' in s:
                sys.exit(u'Onedir mode is not supported')
            else:
                new_spec.append(s)
        with open(spec_file, u'w') as f:
            for n in new_spec:
                f.write(n)
        # End spec file sanitation
    else:
        pyi_args.append(u'-F')
        pyi_args.append(u'--name={}'.format(get_system()))
        pyi_args.append(u'--specpath={}'.format(spec_dir))

    pyi_args.append(u'--distpath={}'.format(new_dir))
    pyi_args.append(u'--workpath={}'.format(work_dir))
    pyi_args.append(u'-y')

    cmds = [u'pyinstaller'] + pyi_args
    exit_code = subprocess.call(cmds)

    if exit_code != 0:
        sys.exit(u'Build Failed')

    # Now archive the file
    with ChDir(new_dir):
        sys_name = get_system()
        if os.path.exists(sys_name + u'.exe'):
            sys_name += u'.exe'
        elif os.path.exists(sys_name + u'.app'):
            os.remove(sys_name)
            sys_name += u'.app'
        name = args.app_name
        version = args.app_version

        # Time for some archive creation!
        file_name = make_archive(name, version, sys_name)
    print(u'\n{} has been placed in your new folder\n'.format(file_name))
    finished = time.time() - start
    print(u'Build finished in {:.2f} seconds.'.format(finished))


def check_version(version):
    match = re.match(u'(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)',
                     version)
    if match is None:
        return False
    else:
        return True


if __name__ == u'__main__':
    args = sys.argv[1:]
    main(args)
