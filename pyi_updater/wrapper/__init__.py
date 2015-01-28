# --------------------------------------------------------------------------
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
# --------------------------------------------------------------------------
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
from pyi_updater.utils import (check_repo,
                               initial_setup,
                               pretty_time,
                               setup_appname,
                               setup_company,
                               setup_urls,
                               setup_patches,
                               setup_scp,
                               setup_s3)
from pyi_updater.wrapper.builder import Builder
from pyi_updater.wrapper.options import get_parser


log = logging.getLogger()
if os.path.exists(os.path.join(os.getcwd(), u'pyiu.log')):
    fh = logging.FileHandler(os.path.join(os.getcwd(), u'pyiu.log'))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(log_format_string())
    log.addHandler(fh)

fmt = logging.Formatter('[%(levelname)s] %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(fmt)
sh.setLevel(logging.DEBUG)
log.addHandler(sh)

CWD = os.getcwd()
loader = Loader()
LOG_DIR = user_log_dir(settings.APP_NAME, settings.APP_AUTHOR)


def clean(args):
    if args.yes is True:
        cleaned = False
        if os.path.exists(settings.CONFIG_DATA_FOLDER):
            cleaned = True
            shutil.rmtree(settings.CONFIG_DATA_FOLDER, ignore_errors=True)
            log.info(u'Removed {} folder'.format(settings.CONFIG_DATA_FOLDER))
        if os.path.exists(settings.USER_DATA_FOLDER):
            cleaned = True
            shutil.rmtree(settings.USER_DATA_FOLDER, ignore_errors=True)
            log.info(u'Removed {} folder'.format(settings.USER_DATA_FOLDER))
        if cleaned is True:
            log.info(u'Clean complete...')
        else:
            log.info(u'Nothing to clean...')
    else:
        log.info(u'Must pass -y to confirm')


def init(args):
    count = args.count
    if count > 10:
        sys.exit(u'Cannot be more then 10')
    if not os.path.exists(os.path.join(settings.CONFIG_DATA_FOLDER,
                          settings.CONFIG_FILE_USER)):
        config = initial_setup(SetupConfig())
        log.info(u'Creating pyi-data dir...')
        pyiu = PyiUpdater(config)
        pyiu.setup()
        log.info(u'Making signing keys...')
        pyiu.make_keys(count)
        config.PUBLIC_KEYS = pyiu.get_public_keys()
        loader.save_config(config)
        log.info(u'Setup complete')
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
            log.info('* Most Recent Revoked Key *')
            log.info('Created: {}'.format(pretty_time(key[u'date'])))
            log.info('Type: {}'.format(key[u'key_type']))
            log.info('Public Key: {}'.format(key[u'public']))
            if args.private is True:
                log.info('Private Key: {}'.format(key[u'private']))
            else:
                log.info(u'Private Key: * Next time to show private key '
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
        old_log_zip = os.path.join(og_dir, settings.DEBUG_ARCHIVE)
        if os.path.exists(old_log_zip):
            os.remove(old_log_zip)
        shutil.move(settings.DEBUG_ARCHIVE, og_dir)
    log.info(u'Log export complete')


def pkg(args):
    check_repo()
    pyiu = PyiUpdater(loader.load_config())
    if args.process is False and args.sign is False:
        sys.exit(u'You must specify a command')

    if args.process is True:
        log.info(u'Processing packages...')
        pyiu.process_packages()
        log.info(u'Processing packages complete')
    if args.sign is True:
        log.info(u'Signing packages...')
        pyiu.sign_update()
        log.info(u'Signing packages complete')


def setter(args):
    check_repo()
    config = loader.load_config()
    if args.appname is True:
        setup_appname(config)
    if args.company is True:
        setup_company(config)
    if args.urls is True:
        setup_urls(config)
    if args.patches is True:
        setup_patches(config)
    if args.scp is True:
        setup_scp(config)
    if args.s3 is True:
        setup_s3(config)
    loader.save_config(config)
    log.info(u'Settings update complete')


def upload(args):
    check_repo()
    upload_service = args.service
    if upload_service is None:
        log.error('Must provide service name')
        sys.exit(1)
    password = os.environ.get('PYIUPDATER_PASS')
    if password is None:
        log.error('You need to set PYIUPDATER_PASS env var')
        sys.exit(1)
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
        log.error(msg)
        sys.exit(1)
    try:
        pyiu.upload()
    except Exception as e:
        msg = (u'Looks like you forgot to add USERNAME '
               'and/or REMOTE_DIR')
        log.debug(str(e), exc_info=True)
        log.error(msg)
        sys.exit(1)


def _real_main(args):
    if args is None:
        args = sys.argv[1:]
    parser = get_parser()
    args, pyi_args = parser.parse_known_args(args)
    cmd = args.command
    if cmd == u'build':
        check_repo()
        builder = Builder(args, pyi_args)
        builder.build()
    elif cmd == u'clean':
        clean(args)
    elif cmd == u'init':
        init(args)
    elif cmd == u'keys':
        keys(args)
    elif cmd == u'log':
        _log(args)
    elif cmd == u'make-spec':
        check_repo()
        builder = Builder(args, pyi_args)
        builder.make_spec(spec_only=True)
    elif cmd == u'pkg':
        pkg(args)
    elif cmd == u'settings':
        setter(args)
    elif cmd == u'upload':
        upload(args)
    elif cmd == u'version':
        print('PyiUpdater {}'.format(__version__))
    else:
        log.error(u'Not Implemented')
        sys.exit(1)


def main(args=None):
    try:
        _real_main(args)
    except KeyboardInterrupt:
        print(u'\n')
        msg = u'Exited by user'
        log.warning(msg)
        sys.exit(1)
    except Exception as err:
        log.debug(str(err), exc_info=True)
        log.error(str(err))
        sys.exit(1)

if __name__ == u'__main__':
    args = sys.argv[1:]
    main(args)
