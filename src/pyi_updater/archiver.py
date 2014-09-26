from __future__ import print_function
import optparse
import os
import shutil
import sys

from jms_utils.terminal import get_terminal_size, terminal_formatter

from pyi_updater.exceptions import ArchiverError
from pyi_updater.utils import (get_version_number,
                               parse_platform,
                               version_string_to_tuple)
from pyi_updater import get_version

max_help_position = 80
max_width = get_terminal_size()[0]

fmt = terminal_formatter()

usage = ('usage: pyi-archive -n "My App" -v 1.0.1 FILE [FILE...]\n'
         'Usage: pyi-archive -i gzip -n "My App" -v 1.0.1 FILE [FILE...]')
kw = {
    'version': get_version(),
    'usage': usage,
    'formatter': fmt,
    'conflict_handler': 'resolve',
    }
parser = optparse.OptionParser(**kw)
parser.add_option('-c', '--archiver',
                  default='zip',
                  type='choice',
                  choices=['zip', 'gzip', 'g', 'z'],
                  help='Type of archive compression to use')

parser.add_option('-n', '--name', help='Name of update')

parser.add_option('-v', '--version-num',
                  help="Version # of update. Must have Major.Minor.Patch "
                  "even if it's 0 eg. 1.1.0")
parser.add_option('--keep',
                  action='store_true',
                  default=False,
                  help='Do not delete source file')

keep = False


def main(my_opts=None):
    global keep
    if my_opts is None:
        opts, args = parser.parse_args(sys.argv)
        keep = opts.keep
        version = check_version(opts)
        name = check_name(opts)
        archiver = opts.archiver
    # Used for testing purposes
    else:
        version = check_version(my_opts)
        name = check_name(my_opts)
        args = my_opts.args
        archiver = my_opts.archiver

    files = []
    not_found_files = []
    not_supported = []
    for f in args[1:]:
        # If I cant find the file or it isn't a supported
        # platform then it gets put on the naughty list
        if not os.path.exists(f):
            not_found_files.append(f)
        elif support_files(f) is False:
            not_supported.appned(f)
        else:
            files.append(f)
    # Used for testing purposes
    if len(files) < 1:
        return False

    for f in files:
        if archiver == 'zip' or archiver == 'z':
            make_archive(name, version, f, 'zip')
        else:
            make_archive(name, version, f, 'gztar')

    # Providing a little feedback
    if len(not_found_files) > 0:
        print('Files not found:')
        for f in not_found_files:
            print(f)
    if len(not_supported) > 0:
        print('Not a supported platform')
        for f in not_supported:
            print(f)
    # Used for testing purposes
    return True


def check_version(options):
    try:
        version = options.version_num
    except:
        raise ArchiverError('You must pass -v option with version # of update',
                            expected=True)

    if version is None:
        raise ArchiverError('You must pass version number')

    try:
        version = get_version_number(version)
    except:
        raise ArchiverError('Can not parse version number',
                            expected=True)

    try:
        version_tuple = version_string_to_tuple(version)
    except:
        raise ArchiverError('Version not in correct format. eg. "0.0.1"',
                            expected=True)

    if len(version_tuple) != 3:
        raise ArchiverError('Version must be MAJOR.MINOR.PATCH',
                            expected=True)
    return version


def check_name(options):
    try:
        name = options.name
    except:
        raise ArchiverError('You must pass -n option with name of update')
        sys.exit(1)
    return name


def make_archive(name, version, file_, archive_format=u'zip', platform=None):
    if platform is None:
        plat = parse_platform(file_)
    else:
        plat = platform
    if archive_format == u'zip':
        ext = u'.zip'
    else:
        ext = u'.tar.gz'

    file_dir = os.path.dirname(os.path.abspath(file_))
    filename = '{}-{}-{}'.format(name, plat, version)

    ext = os.path.splitext(file_)[1]
    temp_file = name + ext

    if os.path.isfile(file_):
        shutil.copy(file_, temp_file)
    else:
        shutil.copytree(file_, temp_file)

    shutil.make_archive(filename, archive_format, file_dir, temp_file)

    if os.path.isfile(temp_file):
        os.remove(temp_file)
    else:
        shutil.rmtree(temp_file, ignore_errors=True)

    if keep is False:
        os.remove(file_)

    return filename + ext


def support_files(f):
    try:
        plat = parse_platform(f)
    except:
        plat = None

    if plat in ['win', 'mac', 'nix', 'nix64', 'arm']:
        return True
    return False

if __name__ == '__main__':
    main()
