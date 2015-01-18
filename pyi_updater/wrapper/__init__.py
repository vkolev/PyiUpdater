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
import shutil
import sys
from zipfile import ZipFile

from appdirs import user_log_dir
from jms_utils.logger import log_format_string
from jms_utils.paths import ChDir
import stevedore

from pyi_updater import PyiUpdater, __version__
from pyi_updater import settings
from pyi_updater.config import Loader, SetupConfig
from pyi_updater.exceptions import UploaderError
from pyi_updater.utils import initial_setup
from pyi_updater.wrapper.builder import Builder
from pyi_updater.wrapper.options import parser
from pyi_updater.wrapper.utils import check_repo, pretty_time

log = logging.getLogger(__name__)
if os.path.exists(os.path.join(os.getcwd(), u'pyiu.log')):
    ch = logging.FileHandler(os.path.join(os.getcwd(), u'pyiu.log'))
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(log_format_string())
    log.addHandler(ch)


CWD = os.getcwd()
loader = Loader()
LOG_DIR = user_log_dir(settings.APP_NAME, settings.APP_AUTHOR)


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


def _log(args):
    og_dir = os.getcwd()
    with ChDir(LOG_DIR):
        files = []
        temp_files = os.listdir(os.getcwd())
        for t in temp_files:
            if t.startswith(settings.LOG_FILENAME_DEBUG):
                log.debug('Adding {} to log'.format(t))
                files.append(t)
        with ZipFile(settings.DEBUG_ARCHIVE, u'w') as zf:
            for f in files:
                log.debug(u'Archiving {}'.format(f))
                zf.write(f)
        shutil.move(settings.DEBUG_ARCHIVE, og_dir)
    print(u'Log export complete')


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
        if len(plugin_names) == 0:
            msg = (u'*** No upload plugins instaled! ***\nYou can install the '
                   u'aws s3 plugin with\n$ pip install pyiupdater[s3]\n\nOr '
                   u'the scp plugin with\n$ pip install pyiupdater[scp]')
        else:
            msg = (u'Invalid Uploader\n\nAvailable options:\n'
                   u'{}'.format(plugin_names))
        sys.exit(msg)
    try:
        pyiu.upload()
    except Exception as e:
        msg = (u'Looks like you forgot to add USERNAME '
               'and/or REMOTE_DIR')
        log.debug(str(e), exc_info=True)
        sys.exit(msg)


def _real_main(args):
    if args is None:
        args = sys.argv[1:]
    args, pyi_args = parser.parse_known_args(args)
    cmd = args.command
    if cmd == u'build':
        builder = Builder(args, pyi_args)
        builder.start()
    elif cmd == u'clean':
        clean(args)
    elif cmd == u'init':
        init(args)
    elif cmd == u'keys':
        keys(args)
    elif cmd == u'log':
        _log(args)
    elif cmd == u'pkg':
        pkg(args)
    elif cmd == u'upload':
        upload(args)
    elif cmd == u'version':
        print(u'PyiUpdater {}'.format(__version__))
    else:
        sys.exit(u'Not Implemented')


def main(args=None):
    try:
        _real_main(args)
    except KeyboardInterrupt:
        msg = u'\nExited by user'
        log.debug(msg)
        sys.exit(msg)
    except Exception as err:
        log.debug(str(err), exc_info=True)
        sys.exit(str(err))

if __name__ == u'__main__':
    args = sys.argv[1:]
    main(args)
