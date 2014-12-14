import argparse
import os
import re
import subprocess
import sys
import time

from jms_utils.paths import ChDir
from jms_utils.system import get_system

from pyi_updater import PyiUpdater, PyiUpdaterConfig
from pyi_updater.config import SetupConfig
from pyi_updater.utils import initial_setup, make_archive
from pyi_updater.version import get_version

start = time.time()

CWD = os.getcwd()

parser = argparse.ArgumentParser(usage=u'%(prog)s')

subparsers = parser.add_subparsers(help=u'commands', dest=u'command')

build_parser = subparsers.add_parser(u'build', help=u'compiles script',
                                     usage=u'%(prog)s <script> [opts]')

init_parser = subparsers.add_parser(u'init', help=u'initializes a '
                                    u'src directory: Not Implemented')

keys_parser = subparsers.add_parser(u'keys', help=u'Manage signing keys: '
                                    u'Not Implemented')


package_parser = subparsers.add_parser(u'pkg', help=u'Manages creation of '
                                       u'file metadata: '
                                       u'Not Implemented')

upload_parser = subparsers.add_parser(u'upload', help=u'Uploads files: '
                                      u'Not Implemented')


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
                          default=False, help=argparse.SUPPRESS)
build_parser.add_argument(u'--onedir', action=u"store_true",
                          default=False, help=argparse.SUPPRESS)

# Just capturing these argument.
# Will be added later to pyinstaller build command
build_parser.add_argument(u'-F', action=u"store_true",
                          default=False, help=argparse.SUPPRESS)
build_parser.add_argument(u'--onefile', action=u"store_true",
                          default=False, help=argparse.SUPPRESS)

# Just capturing these arguments
# ToDo: Take a closer look at this switch
build_parser.add_argument(u'-c', action=u"store_true",
                          default=False, help=argparse.SUPPRESS)
build_parser.add_argument(u'--console', action=u"store_true",
                          default=False, help=argparse.SUPPRESS)
build_parser.add_argument(u'--nowindowed', action=u"store_true",
                          default=False, help=argparse.SUPPRESS)

# Potentially harmful for cygwin on windows
# ToDo: Maybe do a check for cygwin and disable if cygwin is true
build_parser.add_argument(u'-s', action=u"store_true",
                          default=False, help=argparse.SUPPRESS)
build_parser.add_argument(u'--strip', action=u"store_true",
                          default=False, help=argparse.SUPPRESS)
# End of args override

# Used by PyiWrapper
build_parser.add_argument(u'--app-name', dest=u"app_name", required=True)
build_parser.add_argument(u'--app-version', dest=u"app_version", required=True)


def main():
    args = sys.argv[1:]
    args, pyi_args = parser.parse_known_args(args)
    cmd = args.command
    if cmd == u'build':
        builder(args, pyi_args)
    elif cmd == u'init':
        setup()
    elif cmd == u'_upload':
        upload(args)
    elif cmd == u'version':
        print(u'PyiUpdater {}'.format(get_version()))
    else:
        sys.exit(u'Not Implemented')


def setup():
    if not os.path.exists(u'config.data') and not os.path.exists(u'config.data.enc'):
        config = initial_setup(SetupConfig())
        print(u'\nCreating pyi-data dir...\n')
        pyiu = PyiUpdater(PyiUpdaterConfig(config))
        pyiu.setup()
        print(u'\nMaking signing keys...')
        pyiu.make_keys()
        print(u'\nSetup complete')


def upload(args):
    if len(args) > 1:
        sys.exit(u'Can only provide one uploader name')
    try:
        requested_uploader = args[0]
    except IndexError:
        sys.exit(u'Must give name of uploader')


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
    wrapper(args)
