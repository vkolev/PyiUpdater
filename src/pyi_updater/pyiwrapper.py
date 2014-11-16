import os
import re
import sys

from jms_utils.paths import ChDir
from jms_utils.system import get_system

from pyi_updater.archiver import make_archive


def wrapper():
    global sys
    args = sys.argv[1:]
    pyi_dir = os.path.join(os.getcwd(), u'pyi-data')
    new_dir = os.path.join(pyi_dir, u'new')
    if not os.path.exists(pyi_dir):
        sys.exit(u'pyi-data folder not found')
    if not os.path.exists(new_dir):
        sys.exit(u'pyi-data/new folder not found')

    data = _main(args)
    data[u'args'].append(u'-F')
    data[u'args'].append(u'--distpath={}'.format(new_dir))
    data[u'args'].append(u'--name={}'.format(get_system()))
    data[u'args'].append(u'-y')
    pyi_args = u' '.join(data[u'args'])
    command = u'pyinstaller ' + pyi_args
    os.system(command)

    # Now archive the file
    with ChDir(new_dir):
        sys = get_system()
        if os.path.exists(sys + u'.exe'):
            sys += u'.exe'
        elif os.path.exists(sys + u'.app'):
            os.remove(sys)
            sys += u'.app'
        name = data[u'name']
        version = data[u'version']
        if sys == u'win':
            arch = u'zip'
        else:
            arch = u'gzip'

        make_archive(name, version, sys, arch, get_system())


def _main(args=None):
    if args is None or len(args) == 0:
        sys.exit(u'Must pass python script.')
    app_name = None
    app_version = None
    my_re = re.compile(u'(?P<switch>[-]{2}app[-]{1}(name|version)=)'
                       u'"?(?P<value>.*[^"])"?')
    # switch_re = re.compile('(?P<switch>[-]{1,2}[^=\s]*=?)"?'
                           # '(?P<value>.*[^"])"?')

    # Grab required argument values for the wrapper
    remove = []
    for c, a in enumerate(args):
        match = my_re.match(a)
        if match is not None:
            data = match.groupdict()
            if u'switch' in data.keys() and u'value' in data.keys():
                if u'--app-version' in data[u'switch']:
                    remove.append(c)
                    app_version = data[u'value']
                elif u'--app-name' in data[u'switch']:
                    remove.append(c)
                    app_name = data[u'value']

    if app_name is None:
        sys.exit(u'Must pass --app-name="Your App Name"')
    if app_version is None:
        sys.exit(u'Must pass --app-version=0.0.0')

    # Removing arguments & values
    new_args = []
    for a in args:
        if args.index(a) in remove:
            continue
        else:
            new_args.append(a)

    # Looking to change ['-n', 'App'] to ['-n App']
    fixed_args = []
    temp = []
    for n in new_args:
        if u'--' in n:
            fixed_args.append(n)

    for c, n in enumerate(new_args):
        if c == 0:
            fixed_args.append(n)
            continue
        if len(temp) == 2:
            fixed_args.append(' '.join(temp))
            temp = []
        # Adding commands that take no arguments to fixed
        if n in [u'-D', u'--onedir', u'-F', u'--onefile']:
            fixed_args.append(n)
        elif u'--' not in n:
            temp.append(n)

    # Removing args that I plan on overriding or not supported
    temp_args = []
    for n in fixed_args:
        for t in [u'-D', u'--onedir', u'-F', u'--onefile',
                  u'--name', u'-n', u'-o', u'--distpath']:
            if n.startswith(t):
                break
        else:
            temp_args.append(n)

    # Making sure script is the first argument
    pyi_args = []
    for c, t in enumerate(temp_args):
        if t.endswith(u'.py'):
            pyi_args.append(temp_args.pop(c))

    pyi_args += temp_args
    return {
        u'args': pyi_args,
        u'name': app_name,
        u'version': app_version
        }

if __name__ == u'__main__':
    wrapper()
