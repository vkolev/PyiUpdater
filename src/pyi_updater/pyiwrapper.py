import argparse
import os
import re
import sys

from jms_utils.paths import ChDir
from jms_utils.system import get_system

from pyi_updater.archiver import make_archive


parser = argparse.ArgumentParser(usage='%(prog)s [opts] <scriptname>')
parser.add_argument('-o')
parser.add_argument('--distpath')

parser.add_argument('--specpath')

parser.add_argument('--workpath')

parser.add_argument('-n')
parser.add_argument('--name')

parser.add_argument('-D', action="store_true", default=False)
parser.add_argument('--onedir', action="store_true", default=False)

parser.add_argument('-F', action="store_true", default=False)
parser.add_argument('--onefile', action="store_true", default=False)

parser.add_argument('-c', action="store_true", default=False)
parser.add_argument('--console', action="store_true", default=False)
parser.add_argument('--nowindowed', action="store_true", default=False)

parser.add_argument('-s', action="store_true", default=False)
parser.add_argument('--strip', action="store_true", default=False)


parser.add_argument('--app-name', dest="app_name", required=True)
parser.add_argument('--app-version', dest="app_version", required=True)


def wrapper():
    global sys
    args = sys.argv[1:]
    pyi_dir = os.path.join(os.getcwd(), u'pyi-data')
    new_dir = os.path.join(pyi_dir, u'new')
    build_dir = os.path.join(os.getcwd(), '.pyi-cache')
    if not os.path.exists(build_dir):
        os.mkdir(build_dir)

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
    pyi_args.append(u'--specpath={}'.format(build_dir))
    pyi_args.append(u'--workpath={}'.format(build_dir))
    pyi_args.append(u'--name={}'.format(get_system()))
    pyi_args.append(u'-y')

    cmds = [u'pyinstaller'] + pyi_args
    command = ' '.join(cmds)
    os.system(command)

    # Now archive the file
    with ChDir(new_dir):
        sys = get_system()
        if os.path.exists(sys + u'.exe'):
            sys += u'.exe'
        elif os.path.exists(sys + u'.app'):
            os.remove(sys)
            sys += u'.app'
        name = args.app_name
        version = args.app_version
        if sys == u'win':
            arch = u'zip'
        else:
            arch = u'gzip'

        make_archive(name, version, sys, arch, get_system())


def check_version(version):
    match = re.match('(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)',
                     version)
    if match is None:
        return False
    else:
        return True


if __name__ == u'__main__':
    wrapper()
