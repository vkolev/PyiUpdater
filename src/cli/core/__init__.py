from __future__ import print_function
import logging
import os
import pickle
import sys
import time

from six.moves import input

from cli.core import keys, settings, sign, upload
from cli.core.common import CommonLogic
from cli.ui.menu import Menu
from cli.ui.menu_utils import (ask_yes_no, get_correct_answer,
                               path_fixer, _directory_fixer)
from pyi_updater import (FileCrypt, KeyHandler, PyiUpdater,
                         PackageHandler, Uploader)
from pyi_updater.config import SetupConfig
from pyi_updater.utils import cwd_, verify_password

log = logging.getLogger(__name__)


class Worker(Menu, CommonLogic):

    def __init__(self):
        self.file_crypt = FileCrypt()
        self.config = self.load_config()
        self.pyi_updater = PyiUpdater(__name__, self.config)
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
            self.cwd = cwd_
            dec_path = os.path.join(self.cwd, u'config.data')
            enc_path = os.path.join(self.cwd, u'config.data.enc')
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
        self.config.PRIVATE_KEY_NAME = self.config.APP_NAME
        self.config.PUBLIC_KEY_NAME = self.config.APP_NAME

        self.config.COMPANY_NAME = get_correct_answer(u'Please enter your '
                                                      'company or name',
                                                      required=True)

        while 1:
            dev_data_dir = get_correct_answer(u'Enter directory to store'
                                              ' work files',
                                              default=u'Current Working '
                                              'Directory')
            dev_data_dir = _directory_fixer(dev_data_dir)
            if os.access(dev_data_dir, os.W_OK) and os.access(dev_data_dir,
                                                              os.R_OK):
                self.config.DEV_DATA_DIR = path_fixer(dev_data_dir)
                break
            else:
                self.display_msg(u'You do not have read/write permission '
                                 'for this directory')
                self.display_msg(u'Press Enter to try a different directory')
                input()

        while 1:
            key_length = get_correct_answer(u'Enter a key length. Longer is '
                                            'more secure but takes longer '
                                            'to compute. Must be multiple '
                                            'of 256!', default=u'2048')
            if int(key_length) % 256 == 0:
                self.config.KEY_LENGTH = key_length
                break
            input('Must be a multiple of 256!! Press enter to try again.')

        self.config.UPDATE_URL = get_correct_answer(u'Enter your update url',
                                                    required=True)

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
        try:
            self.file_crypt.decrypt()
        except Exception as e:
            log.warning(u'Might be nothing to decrypt yet')
            log.error(str(e), exc_info=True)
        with open(filename, 'w') as f:
            f.write(str(pickle.dumps(obj)))
        self.file_crypt.encrypt()

    def load_config(self):
        log.debug(u'Loading Config')
        filename = os.path.join(cwd_, u'config.data')
        self.file_crypt.new_file(filename)
        try:
            self.file_crypt.decrypt()
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
