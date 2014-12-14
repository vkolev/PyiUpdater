from __future__ import print_function
import logging
import os
import pickle
import sys
import time

from cli_ui.core import keys, settings, sign, upload
from cli_ui.core.common import CommonLogic
from cli_ui.ui.menu import Menu

from pyi_updater import PyiUpdater, PyiUpdaterConfig
from pyi_updater.config import SetupConfig
from pyi_updater.exceptions import FileCryptPasswordError
from pyi_updater.filecrypt import FileCrypt
from pyi_updater.utils import (initial_setup,
                               verify_password)

log = logging.getLogger(__name__)


CWD = os.getcwd()


class Worker(Menu, CommonLogic):

    def __init__(self):
        self.file_crypt = FileCrypt()
        self.config = self.load_config()
        self.pyi_config = PyiUpdaterConfig(self.config)
        self.pyiu = PyiUpdater()
        self.update_helpers(self.pyi_config)

        helpers = {
            u'file_crypt': self.file_crypt,
            u'config': self.pyi_config,
            u'save': self.save_config,
            u'pyiu': self.pyiu
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

    def update_helpers(self, pyi_updater):
        self.pyiu.update_config(pyi_updater)
        self.file_crypt.init_app(pyi_updater)
        self.pyiu.add_filecrypt(self.file_crypt)
        log.debug(u'Updated helpers')

    def start(self):
        while 1:
            dec_path = os.path.join(CWD, u'config.data')
            enc_path = os.path.join(CWD, u'config.data.enc')
            if not os.path.exists(dec_path) and not os.path.exists(enc_path):
                self.setup()

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
        lex_file = os.path.join(CWD, u'lextab.py')
        yac_file = os.path.join(CWD, u'yacctab.py')
        if os.path.exists(lex_file):
            os.remove(lex_file)
        if os.path.exists(yac_file):
            os.remove(yac_file)

        log.debug('Quitting')
        print('See Ya!')
        sys.exit()

    def setup(self):
        log.debug(u'Starting initial setup')
        self.display_menu_header(u'Setup Assistant')
        self.display_msg(u'Let\'s begin...')

        self.pyi_config = initial_setup(self.pyi_config)
        self.update_helpers(self.pyi_config)
        self.pyiu.setup()

        password = verify_password(u'Enter password')
        self.file_crypt._update_timer()
        self.save_config(self.pyi_config, password)
        print(u'Making signing keys...')
        self.keys_menu.make_keys()
        self.display_menu_header(u'Setup Complete')
        self.display_msg(u'Now let\'s update some apps')
        time.sleep(3)

    def save_config(self, obj, password=None):
        self.pyi_config.update_config(obj)
        self.update_helpers(self.pyi_config)
        log.debug(u'Saving Config')
        filename = os.path.join(CWD, u'config.data')
        self.file_crypt.new_file(filename)
        # We do this here to keep from asking users
        # password again when we encrypt the file
        if password is not None:
            password = self.file_crypt._gen_password(password)
            self.file_crypt.password = password
        with open(filename, 'w') as f:
            f.write(str(pickle.dumps(obj)))
        self.file_crypt.encrypt()
        self.write_config_py(obj)

    def load_config(self):
        log.debug(u'Loading Config')
        filename = os.path.join(CWD, u'config.data')
        salt_file = os.path.join(CWD, u'pyi-data', u'keys', u'salt')
        self.file_crypt.salt_file = salt_file
        self.file_crypt.new_file(filename)
        try:
            self.file_crypt.decrypt()
        except FileCryptPasswordError:
            sys.exit(u'Failed password attempt')
        except Exception as e:
            log.error(str(e), exc_info=True)
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
        filename = os.path.join(CWD, u'client_config.py')
        attr_str_format = "    {} = '{}'\n"
        attr_format = "    {} = {}\n"
        with open(filename, u'w') as f:
            f.write('class ClientConfig(object):\n')
            if hasattr(obj, 'APP_NAME') and obj.APP_NAME is not None:
                f.write(attr_str_format.format('APP_NAME', obj.APP_NAME))
            if hasattr(obj, 'COMPANY_NAME') and obj.COMPANY_NAME is not None:
                f.write(attr_str_format.format('COMPANY_NAME',
                        obj.COMPANY_NAME))
            if hasattr(obj, 'UPDATE_URLS') and obj.UPDATE_URLS is not None:
                f.write(attr_format.format('UPDATE_URLS', obj.UPDATE_URLS))
            if hasattr(obj, 'PUBLIC_KEY') and obj.PUBLIC_KEY is not None:
                f.write(attr_str_format.format('PUBLIC_KEY', obj.PUBLIC_KEY))
