from __future__ import print_function
import logging
import shutil
import os
import time

from jms_utils.paths import cwd
from six.moves import input

from cli_ui.core.common import CommonLogic
from cli_ui.ui.menu import Menu
from cli_ui.ui.menu_utils import get_correct_answer
from pyi_updater.utils import verify_password


log = logging.getLogger(__name__)


class Settings(CommonLogic, Menu):

    def __init__(self, helpers):
        self.unpack_helpers(helpers)

        header = u'Settings'
        options = [(u'View Settings', self.view_settings),
                   (u'Add Url', self.add_url),
                   (u'Update Settings', self.update_settings),
                   (u'Copy Decrypted Config File', self.copy_decrypted_config),
                   (u'Change Encryption Password', self.change_password),
                   (u'Go Back', self.done)]
        super(Settings, self).__init__(header, options)

    def view_settings(self):
        log.debug(u'View Settings Menu')
        self.display_menu_header(u'View Settings')
        for k, v in self.config.__dict__.items():
            if k.isupper():
                print(k.ljust(20), v)
        input(u'\nPress enter to continue')
        self()

    def add_url(self):
        self.display_menu_header('Add Url')
        url = get_correct_answer('Enter url to add.')
        self.config.UPDATE_URLS.append(url)
        self.config.UPDATE_URLS = list(set(self.config.UPDATE_URLS))
        self.save(self.config)
        input(u'\nUrl added. Press enter to continue')
        self()

    def update_settings(self):
        log.debug(u'Update Settings Menu')
        self.display_menu_header(u'Update Settings')
        msg = (u'Enter the number of each item you\'d like to update.')
        self.display_msg(msg)
        self.display_msg(u'Examples:')
        self.display_msg(u'-->13 ')
        self.display_msg(u'-->235 ')
        self.display_msg(u'-->513')
        self.display_msg(u'Then press Enter')
        print((u'1. App Name\n'
               '2. Company Name\n'
               '3. Username\n'
               '4. Password\n'
               '5. ssh key path\n'
               '6. Remote dir or bucket name\n'
               '7. Host settings\n'))
        answers = input(u'-->')

        self.display_menu_header(u'Updating Settings')
        if '1' in answers:
            app_name = get_correct_answer(u'Enter APP NAME',
                                          default=self.config.APP_NAME)
            self.config.APP_NAME = app_name
        if '2' in answers:
            if not hasattr(self.config, u'COMPANY_NAME'):
                self.config.COMPANY_NAME = None
            company_name = get_correct_answer(u'Enter Company Name',
                                              default=self.config.COMPANY_NAME)
            self.config.COMPANY_NAME = company_name

        if '3' in answers:
            username = get_correct_answer(u'Enter new username',
                                          default=self.config.USERNAME)
            self.config.USERNAME = username

        if '4' in answers:
            password = get_correct_answer(u'Enter new password',
                                          default=self.config.PASSWORD)
            self.config.PASSWORD = password

        if '5' in answers:
            password = get_correct_answer(u'Enter new ssh key path',
                                          default=self.config.PASSWORD)
            self.config.PASSWORD = password
        if '6' in answers:
            r_dir = get_correct_answer(u'Enter new remote directory or bucket',
                                       default=self.config.REMOTE_DIR)
            self.config.REMOTE_DIR = r_dir

        if '7' in answers:
            host = get_correct_answer(u'Enter host name or ip',
                                      default=self.config.HOST)
            self.config.HOST = host

        self.save(self.config)
        print(u'Saving new config....')
        time.sleep(3)
        self()

    def copy_decrypted_config(self):
        log.debug(u'Attempting to copy decrypted config')
        filename = os.path.join(cwd, u'config.data')
        self.file_crypt.new_file(filename)
        self.file_crypt.decrypt()
        try:
            shutil.copy(filename, filename + u' copy')
        except Exception as e:
            log.error(str(e), exc_info=True)
            log.error(u'Cannot copy decrypted config file')
        self.file_crypt.encrypt()
        msg = u'Decrypted config file copied.  Press enter to continue'
        # May be casing an issue with cli
        # self.display_msg(msg)
        input(msg)
        self()

    def change_password(self):
        private_key_path = os.path.join(self.key_handler.keys_dir,
                                        self.key_handler.private_key_name)
        config_path = os.path.join(cwd, u'config.data')

        old_pass = verify_password('Enter old password')
        new_pass = verify_password('Enter new password')

        # Start private key password change
        self.file_crypt.new_file(private_key_path)
        success = self.file_crypt.change_password(old_pass, new_pass)
        if success is False:
            input('Password is not correct. Press Enter to return')
            self()
        self.file_crypt.new_file(config_path)
        success = self.file_crypt.change_password(old_pass, new_pass)
        input('Password change complete. Press enter to continue.')
        self()
