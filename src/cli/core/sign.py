import logging
import time

from cli.core.common import CommonLogic
from cli.ui.menu import Menu


log = logging.getLogger(__name__)


class Sign(CommonLogic, Menu):

    def __init__(self, helpers):
        self.unpack_helpers(helpers)

        header = u'Sign Updates'
        message = (u'Make sure updates are in "new" folder '
                   'then press "1" to start.')

        options = [(u'Start', self.start_sign_updates),
                   (u'Main Menu', self.done)]
        super(Sign, self).__init__(header, options, message)

    def start_sign_updates(self):
        s_menu = Menu()
        s_menu.display_menu_header(u'Signing updates...')
        s_menu.display_msg(u'Please wait...')

        self.package_handler.setup()
        self.package_handler.process_packages()
        self.key_handler.sign_update()

        s_menu.display_msg(u'Update signing complete...')
        time.sleep(3)
