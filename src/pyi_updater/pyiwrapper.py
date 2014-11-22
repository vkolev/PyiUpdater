import argparse
import os
import re
import sys
import time

from jms_utils.paths import ChDir
from jms_utils.system import get_system

from pyi_updater.utils import make_archive


start = time.time()
parser = argparse.ArgumentParser(usage='%(prog)s [opts] <scriptname>')

# Start of args override
# This will be set to the pyi-data/new directory.
# When we make the final compressed archive we will look
# for an exe in that dir.
parser.add_argument('-o')
parser.add_argument('--distpath')

# Will be set to .pyiupdater/spec/
# Trying to keep root dir clean
parser.add_argument('--specpath')

# Will be set to .pyiupdater/build
# Trying to keep root dir clean
parser.add_argument('--workpath')

# Will be set to platform name i.e. mac, win, nix, nix64, arm\
# When archiving we will change the name to the value passed to
# --app-name
parser.add_argument('-n')
parser.add_argument('--name')

# Just capturing these argument.
# PyiUpdater only supports onefile mode at the moment
parser.add_argument('-D', action="store_true", default=False)
parser.add_argument('--onedir', action="store_true", default=False)

# Just capturing these argument.
# Will be added later to pyinstaller build command
parser.add_argument('-F', action="store_true", default=False)
parser.add_argument('--onefile', action="store_true", default=False)

# Just capturing these arguments
# ToDo: Take a closer look at this switch
parser.add_argument('-c', action="store_true", default=False)
parser.add_argument('--console', action="store_true", default=False)
parser.add_argument('--nowindowed', action="store_true", default=False)

# Potentially harmful for cygwin on windows
# ToDo: Maybe do a check for cygwin and disable if cygwin is true
parser.add_argument('-s', action="store_true", default=False)
parser.add_argument('--strip', action="store_true", default=False)
# End of args override

# Used by PyiWrapper
parser.add_argument('--app-name', dest="app_name", required=True)
parser.add_argument('--app-version', dest="app_version", required=True)


def main():
    args = sys.argv[1:]
    wrapper(args)


def wrapper(args):
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

    args, pyi_args = parser.parse_known_args(args)
    if check_version(args.app_version) is False:
        sys.exit(u"""Error: version # needs to be in the form of "0.10.0"

    Visit url for more info:

        http://semver.org/
                  """)

    for p in pyi_args:
        if p.endswith(u'.py'):
            break
    else:
        sys.exit(u'Must pass a python script')

    pyi_args.append(u'-F')
    pyi_args.append(u'--distpath={}'.format(new_dir))
    pyi_args.append(u'--specpath={}'.format(spec_dir))
    pyi_args.append(u'--workpath={}'.format(work_dir))
    pyi_args.append(u'--name={}'.format(get_system()))
    pyi_args.append(u'-y')

    cmds = [u'pyinstaller'] + pyi_args
    command = ' '.join(cmds)
    os.system(command)

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
