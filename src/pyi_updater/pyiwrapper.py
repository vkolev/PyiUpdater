import argparse
import os
import re
import subprocess
import sys
import time

from jms_utils.paths import ChDir
from jms_utils.system import get_system

from pyi_updater.utils import make_archive
from pyi_updater.version import get_version

start = time.time()
parser = argparse.ArgumentParser(usage='%(prog)s')

subparsers = parser.add_subparsers(help='commands', dest=u'command')

init_parser = subparsers.add_parser(u'init', help=u'initializes a '
                                    'src directory: Not Implemented')

build_parser = subparsers.add_parser(u'build', help=u'compiles script',
                                     usage=u'%(prog)s <script> [opts]')

upload_parser = subparsers.add_parser(u'upload', help=u'Uploads files: '
                                      'Not Implemented')

keys_parser = subparsers.add_parser(u'keys', help=u'Manage signing keys: '
                                    'Not Implemented')

package_parser = subparsers.add_parser(u'pkg', help=u'Manages creation of '
                                       u'file metadata: '
                                       'Not Implemented')

version_parser = subparsers.add_parser(u'version', help=u'Programs version')

# Start of args override
# This will be set to the pyi-data/new directory.
# When we make the final compressed archive we will look
# for an exe in that dir.
build_parser.add_argument('-o', help=argparse.SUPPRESS)
build_parser.add_argument('--distpath', help=argparse.SUPPRESS)

# Will be set to .pyiupdater/spec/
# Trying to keep root dir clean
build_parser.add_argument('--specpath', help=argparse.SUPPRESS)

# Will be set to .pyiupdater/build
# Trying to keep root dir clean
build_parser.add_argument('--workpath', help=argparse.SUPPRESS)

# Will be set to platform name i.e. mac, win, nix, nix64, arm\
# When archiving we will change the name to the value passed to
# --app-name
build_parser.add_argument('-n', help=argparse.SUPPRESS)
build_parser.add_argument('--name', help=argparse.SUPPRESS)

# Just capturing these argument.
# PyiUpdater only supports onefile mode at the moment
build_parser.add_argument('-D', action="store_true",
                          default=False, help=argparse.SUPPRESS)
build_parser.add_argument('--onedir', action="store_true",
                          default=False, help=argparse.SUPPRESS)

# Just capturing these argument.
# Will be added later to pyinstaller build command
build_parser.add_argument('-F', action="store_true",
                          default=False, help=argparse.SUPPRESS)
build_parser.add_argument('--onefile', action="store_true",
                          default=False, help=argparse.SUPPRESS)

# Just capturing these arguments
# ToDo: Take a closer look at this switch
build_parser.add_argument('-c', action="store_true",
                          default=False, help=argparse.SUPPRESS)
build_parser.add_argument('--console', action="store_true",
                          default=False, help=argparse.SUPPRESS)
build_parser.add_argument('--nowindowed', action="store_true",
                          default=False, help=argparse.SUPPRESS)

# Potentially harmful for cygwin on windows
# ToDo: Maybe do a check for cygwin and disable if cygwin is true
build_parser.add_argument('-s', action="store_true",
                          default=False, help=argparse.SUPPRESS)
build_parser.add_argument('--strip', action="store_true",
                          default=False, help=argparse.SUPPRESS)
# End of args override

# Used by PyiWrapper
build_parser.add_argument('--app-name', dest="app_name", required=True)
build_parser.add_argument('--app-version', dest="app_version", required=True)


def main():
    args = sys.argv[1:]
    args, pyi_args = parser.parse_known_args(args)
    cmd = args.command
    if cmd == u'build':
        builder(args, pyi_args)
    elif cmd == u'init':
        pass
    elif cmd == u'upload':
        upload(args)
    elif cmd == u'version':
        print('PyiUpdater {}'.format(get_version()))


def upload(args):
    if len(args) > 1:
        sys.exit('Can only provide one uploader name')
    try:
        requested_uploader = args[0]
    except IndexError:
        sys.exit('Must give name of uploader')


def builder(args, pyi_args):
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
        fix = "\t\t\t\t\tname='{}',".format(get_system())

        # Sanitizing spec file
        with open(spec_file, u'r') as f:
            spec_data = f.readlines()

        new_spec = []
        for s in spec_data:
            # Will replace name with system arch
            # Used for later archiving
            if 'name=' in s:
                new_spec.append(fix)
            elif 'coll' in s or 'COLLECT' in s:
                sys.exit('Onedir mode is not supported')
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
        sys.exit('Build Failed')

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
    print('\n{} has been placed in your new folder\n'.format(file_name))
    finished = time.time() - start
    print('Build finished in {:.2f} seconds.'.format(finished))


def check_version(version):
    match = re.match('(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)',
                     version)
    if match is None:
        return False
    else:
        return True


if __name__ == u'__main__':
    args = sys.argv[1:]
    wrapper(args)
