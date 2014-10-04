from __future__ import print_function
import logging
import os
import pickle
import sys
import time

from cli.core import keys, settings, sign, upload
from cli.core.common import CommonLogic
from cli.ui.menu import Menu
from cli.ui.menu_utils import (ask_yes_no, get_correct_answer,
                               _directory_fixer)

from pyi_updater import PyiUpdater
from pyi_updater.config import SetupConfig
from pyi_updater.exceptions import FileCryptPasswordError
from pyi_updater.filecrypt import FileCrypt
from pyi_updater.key_handler import KeyHandler
from pyi_updater.package_handler import PackageHandler
from pyi_updater.uploader import Uploader
from pyi_updater.utils import cwd_, verify_password

log = logging.getLogger(__name__)


class Worker(Menu, CommonLogic):

    def __init__(self):
        self.file_crypt = FileCrypt()
        self.config = self.load_config()
        self.pyi_updater = PyiUpdater(self.config)
        self.key_handler = KeyHandler()
        self.package_handler = PackageHandler()
        self.uploader = Uploader()
        self.update_helpers(self.pyi_updater)

        helpers = {
            u'key_handler': self.key_handler,
            u'package_handler': self.package_handler,
            u'uploader': self.uploader,
            u'file_crypt': self.file_crypt,
            u'config': self.config,
            u'save': self.save_config,
            }

        self.keys_menu = keys.Keys(helpers)
        self.settings_menu = settings.Settings(helpers)
        self.sign_menu = sign.Sign(helpers)
        self.upload_menu = upload.Upload(helpers)

        header = u'Main Menu'
        options = [(u'Sign Updates', self.sign_menu),
                   (u'Upload', self.upload_menu), (u'Keys', self.keys_menu),
                   (u'Settings', self.settings_menu), (u'Quit', self.quit)]
        super(Worker, self).__init__(header, options)
        # self.menu = Menu(header, options)

    def update_helpers(self, pyi_updater):
        self.key_handler.init_app(pyi_updater)
        self.key_handler._add_filecrypt(self.file_crypt)
        self.package_handler.init_app(pyi_updater)
        self.uploader.init_app(pyi_updater)
        log.debug(u'Updated helpers')

    def start(self):
        while 1:
            dec_path = os.path.join(cwd_, u'config.data')
            enc_path = os.path.join(cwd_, u'config.data.enc')
            if not os.path.exists(dec_path) and not os.path.exists(enc_path):
                self.initial_setup()

            x = self.display()
            if len(x) == 2:
                next_ = x[1]
                next_()
            # We are dynamically generating upload options
            # from installed plugins. So the option selected
            # by the user needs a little extra processing
            else:
                name = x[0]
                func = x[1]
                func(name)

    def quit(self):
        lex_file = os.path.join(cwd_, u'lextab.py')
        yac_file = os.path.join(cwd_, u'yacctab.py')
        if os.path.exists(lex_file):
            os.remove(lex_file)
        if os.path.exists(yac_file):
            os.remove(yac_file)

        log.debug('Quitting')
        print('See Ya!')
        sys.exit()

    def initial_setup(self):
        log.debug(u'Starting initial setup')
        self.display_menu_header(u'Setup Assistant')
        self.display_msg(u'Let\'s begin...')

        self.config.APP_NAME = get_correct_answer(u'Please enter app name',
                                                  required=True)

        self.config.COMPANY_NAME = get_correct_answer(u'Please enter your '
                                                      'company or name',
                                                      required=True)

        self.config.DEV_DATA_DIR = cwd_

        url = get_correct_answer(u'Enter a url to ping for updates.',
                                 required=True)
        self.config.UPDATE_URLS = [url]
        while 1:
            answer = ask_yes_no(u'Would you like to add another '
                                'url for backup?', default='no')
            if answer is True:
                url = get_correct_answer(u'Enter another url.',
                                         required=True)
                self.config.UPDATE_URLS.append(url)
            else:
                break

        self.config.UPDATE_PATCHES = ask_yes_no(u'Would you like to enable '
                                                'patch updates?',
                                                default='yes')

        answer1 = ask_yes_no(u'Would you like to add scp settings?',
                             default='no')

        answer2 = ask_yes_no(u'Would you like to add S3 settings?',
                             default='no')

        if answer1:
            self.config.REMOTE_DIR = get_correct_answer(u'Enter remote dir',
                                                        required=True)
            self.config.HOST = get_correct_answer(u'Enter host', required=True)

            self.config.USERNAME = get_correct_answer(u'Enter usernmae',
                                                      required=True)

            key_path = get_correct_answer(u'Enter path to ssh key',
                                          required=True)
            # Path to private key
            self.config.PASSWORD = _directory_fixer(key_path)

        if answer2:
            self.config.USERNAME = get_correct_answer(u'Enter access key ID',
                                                      required=True)
            self.config.PASSWORD = get_correct_answer(u'Enter secret '
                                                      'Access Key',
                                                      required=True)

            self.config.REMOTE_DIR = get_correct_answer(u'Enter bucket name',
                                                        required=True)

        password = verify_password(u'Enter password')

        self.save_config(self.config, password)
        self.package_handler.setup()
        print(u'Making keys...')
        self.keys_menu.make_keys()
        self.display_menu_header(u'Setup Complete')
        self.display_msg(u'Now let\'s update some apps')
        time.sleep(3)

    def save_config(self, obj, password=None):
        self.pyi_updater.update_config(obj)
        self.update_helpers(self.pyi_updater)
        log.debug(u'Saving Config')
        filename = os.path.join(cwd_, u'config.data')
        self.file_crypt.new_file(filename)
        # We do this here to keep from asking users
        # password again when we encrypt the file
        if password is not None:
            self.file_crypt.password = password
        with open(filename, 'w') as f:
            f.write(str(pickle.dumps(obj)))
        self.file_crypt.encrypt()
        self.write_config_py(obj)

    def load_config(self):
        log.debug(u'Loading Config')
        filename = os.path.join(cwd_, u'config.data')
        self.file_crypt.new_file(filename)
        try:
            self.file_crypt.decrypt()
        except FileCryptPasswordError:
            sys.exit(u'Failed password attempt')
        except Exception as e:
            log.error(str(e))
            log.warning(u'No enc file. Will try to load plain config')
        try:
            with open(filename, 'r') as f:
                config_data = pickle.loads(f.read())
            self.file_crypt.encrypt()
        except Exception as e:
            log.error(e, exc_info=True)
            config_data = SetupConfig()

        return config_data

    def write_config_py(self, obj):
        filename = os.path.join(cwd_, u'client_config.py')
        attr_str_format = "    {} = '{}'\n"
        with open(filename, u'w') as f:
            f.write('class ClientConfig(object):\n')
            if hasattr(obj, 'APP_NAME') and obj.APP_NAME is not None:
                f.write(attr_str_format.format('APP_NAME', obj.APP_NAME))
            if hasattr(obj, 'COMPANY_NAME') and obj.COMPANY_NAME is not None:
                f.write(attr_str_format.format('COMPANY_NAME',
                        obj.COMPANY_NAME))
            if hasattr(obj, 'UPDATE_URL') and obj.UPDATE_URL is not None:
                f.write(attr_str_format.format('UPDATE_URL', obj.UPDATE_URL))
            if hasattr(obj, 'PUBLIC_KEY') and obj.PUBLIC_KEY is not None:
                f.write(attr_str_format.format('PUBLIC_KEY', obj.PUBLIC_KEY))
