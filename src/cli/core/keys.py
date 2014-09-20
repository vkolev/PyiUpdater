import logging

from six.moves import input

from cli.core.common import CommonLogic
from cli.ui.menu import Menu


log = logging.getLogger(__name__)


class Keys(CommonLogic, Menu):

    def __init__(self, helpers):
        self.unpack_helpers(helpers)

        header = u'Keys'
        options = [(u'Show Public Key', self.show_public_key),
                   (u'Make Decrypted Copy of Private Key',
                    self.private_key_copy),
                   (u'Main Menu', self.done)]

        super(Keys, self).__init__(header, options)

    def show_public_key(self):
        log.debug(u'Show public key')
        self.key_handler.print_public_key()
        self.display_msg(u'Press enter to continue')
        input()
        self()

    def private_key_copy(self):
        log.debug(u'Copied private key')
        self.key_handler.copy_decrypted_private_key()
        msg = u'Private key decrypted. Press enter to continue'
        self.display_msg(msg)
        input()
        self()

    def replace_keys(self):
        log.debug(u'Replacing keys')
        self.key_handler.make_keys(overwrite=True)

    def make_keys(self):
        log.debug(u'Making keys')
        self.key_handler.make_keys()
        pub_key = self.key_handler.get_public_key()
        self.config.PUBLIC_KEY = pub_key
        self.save(self.config)
