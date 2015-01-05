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


import logging
import os
import re
import shutil
import subprocess
import sys
import time

from jms_utils.logger import log_format_string
from jms_utils.paths import ChDir
from jms_utils.system import get_system
import stevedore

log = logging.getLogger()
log.setLevel(logging.DEBUG)
fmt_str = log_format_string()
nh = logging.NullHandler()
nh.setLevel(logging.DEBUG)
log.addHandler(nh)

from pyi_updater import PyiUpdater, __version__
from pyi_updater.config import Loader, SetupConfig
from pyi_updater.exceptions import UploaderError
from pyi_updater import settings
from pyi_updater.utils import initial_setup, make_archive
from pyi_updater.wrapper.options import parser

if os.path.exists(os.path.join(os.getcwd(), settings.LOG_FILENAME)):
    ch = logging.FileHandler(os.path.join(os.getcwd(), settings.LOG_FILENAME))
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(log_format_string())
    log.addHandler(ch)

start = time.time()
CWD = os.getcwd()
loader = Loader()


def build(args, pyi_args):
    check_repo()
    pyi_dir = os.path.join(os.getcwd(), settings.USER_DATA_FOLDER)
    new_dir = os.path.join(pyi_dir, u'new')
    build_dir = os.path.join(os.getcwd(), settings.CONFIG_DATA_FOLDER)
    spec_dir = os.path.join(build_dir, u'spec')
    work_dir = os.path.join(build_dir, u'work')
    for d in [build_dir, spec_dir, work_dir, pyi_dir, new_dir]:
        if not os.path.exists(d):
            log.debug(u'Creating directory: {}'.format(d))
            os.mkdir(d)

    if check_version(args.app_version) is False:
        sys.exit(u"""Error: version # needs to be in the form of "0.10.0"

    Visit url for more info:

        http://semver.org/
                  """)

    app_type = None
    for p in pyi_args:
        if p.endswith(u'.py'):
            log.debug(u'Building from python source file')
            app_type = u'script'
            break
        elif p.endswith(u'.spec'):
            log.debug(u'Building from spec file: {}'.format(p))
            spec_file = p
            app_type = u'spec'
            break
    else:
        log.debug(u'No accepted files passed to builder')
        sys.exit(u'Must pass a python script or spec file')

    temp_name = get_system()
    if app_type == u'spec':
        if temp_name == u'win':
            log.debug(u'On windows: Adding .exe extension')
            temp_name += u'.exe'
        fix = u"\t\t\t\t\tname='{}',\n".format(temp_name)

        # Sanitizing spec file
        log.debug(u'Opening spec file')
        with open(spec_file, u'r') as f:
            spec_data = f.readlines()

        new_spec = []
        for s in spec_data:
            # Will replace name with system arch
            # Used for later archiving
            if u'name=' in s:
                regex = re.compile('name=(?P<id>(\'|").*(\'|")),')
                match = regex.search(s)
                name = match.groupdict()['id']
                log.debug(u'App name in spec file: {}'.format(name))
                new_spec.append(fix)
            elif u'coll' in s or u'COLLECT' in s:
                log.debug(u'One dir mode not supported')
                sys.exit(u'Onedir mode is not supported')
            else:
                new_spec.append(s)
        log.debug(u'Writing spec file to disk')
        with open(spec_file, u'w') as f:
            for n in new_spec:
                f.write(n)
        # End spec file sanitation
    else:
        log.debug(u'Adding params to command')
        pyi_args.append(u'-F')
        pyi_args.append(u'--name={}'.format(temp_name))
        pyi_args.append(u'--specpath={}'.format(spec_dir))

    pyi_args.append(u'--distpath={}'.format(new_dir))
    pyi_args.append(u'--workpath={}'.format(work_dir))
    pyi_args.append(u'-y')

    cmds = [u'pyinstaller'] + pyi_args
    log.debug(u'Command: {}'.format(cmds))
    exit_code = subprocess.call(cmds)

    if exit_code != 0:
        log.debug(u'Build failed with status: {}'.format(exit_code))
        sys.exit(u'Build Failed')

    # Now archive the file
    with ChDir(new_dir):
        if os.path.exists(temp_name + u'.app'):
            app_name = temp_name + u'.app'
            name = args.app_name
        elif os.path.exists(temp_name + u'.exe'):
            app_name = temp_name + u'.exe'
            name = args.app_name
        else:
            app_name = temp_name
            name = args.app_name
        log.debug(u'Appname: {}'.format(app_name))
        version = args.app_version

        # Time for some archive creation!
        file_name = make_archive(name, version, app_name)
        log.debug(u'Archive name: {}'.format(file_name))
        if args.keep is False:
            if os.path.exists(temp_name):
                os.remove(temp_name)
    print(u'\n{} has been placed in your new folder\n'.format(file_name))
    finished = time.time() - start
    print(u'Build finished in {:.2f} seconds.'.format(finished))


def clean(args):
    if args.yes is True:
        cleaned = False
        if os.path.exists(settings.CONFIG_DATA_FOLDER):
            cleaned = True
            shutil.rmtree(settings.CONFIG_DATA_FOLDER, ignore_errors=True)
            print(u'Removed {} folder'.format(settings.CONFIG_DATA_FOLDER))
        if os.path.exists(settings.USER_DATA_FOLDER):
            cleaned = True
            shutil.rmtree(settings.USER_DATA_FOLDER, ignore_errors=True)
            print(u'Removed {} folder'.format(settings.USER_DATA_FOLDER))
        if cleaned is True:
            print(u'Clean complete...')
        else:
            print(u'Nothing to clean...')
    else:
        print(u'Must pass -y to confirm')


def init(args):
    count = args.count
    if count > 10:
        sys.exit(u'Cannot be more then 10')
    if not os.path.exists(os.path.join(settings.CONFIG_DATA_FOLDER,
                          settings.CONFIG_FILE_USER)):
        config = initial_setup(SetupConfig())
        print(u'\nCreating pyi-data dir...\n')
        pyiu = PyiUpdater(config)
        pyiu.setup()
        print(u'\nMaking signing keys...')
        pyiu.make_keys(count)
        config.PUBLIC_KEYS = pyiu.get_public_keys()
        loader.save_config(config)
        print(u'\nSetup complete')
    else:
        sys.exit(u'Not an empty PyiUpdater repository')


def keys(args):
    check_repo()
    config = loader.load_config()
    pyiu = PyiUpdater(config)
    if args.revoke is not None:
        count = args.revoke
        pyiu.revoke_key(count)
        config.PUBLIC_KEYS = pyiu.get_public_keys()
        key = pyiu.get_recent_revoked_key()
        if key is not None:
            print('* Most Recent Revoked Key *\n')
            print('Created: {}'.format(pretty_time(key[u'date'])))
            print('Type: {}'.format(key[u'key_type']))
            print('Public Key: {}'.format(key[u'public']))
            if args.private is True:
                print('Private Key: {}'.format(key[u'private']))
            else:
                print(u'Private Key: * Next time to show private key '
                      u'use --show-private *')
    loader.save_config(config)


def pkg(args):
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


def check_repo():
    if not os.path.exists(settings.CONFIG_DATA_FOLDER):
        sys.exit('Not a PyiUpdater repo: Must init first.')


def check_version(version):
    match = re.match(u'(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)',
                     version)
    if match is None:
        return False
    else:
        return True


def pretty_time(sec):
    return time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime(sec))


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    args, pyi_args = parser.parse_known_args(args)
    cmd = args.command
    if cmd == u'build':
        build(args, pyi_args)
    elif cmd == u'clean':
        clean(args)
    elif cmd == u'init':
        init(args)
    elif cmd == u'keys':
        keys(args)
    elif cmd == u'pkg':
        pkg(args)
    elif cmd == u'up':
        upload(args)
    elif cmd == u'version':
        print(u'PyiUpdater {}'.format(__version__))
    else:
        sys.exit(u'Not Implemented')


if __name__ == u'__main__':
    args = sys.argv[1:]
    main(args)
