import logging
import time

from six.moves import input
from stevedore.extension import ExtensionManager

from cli.core.common import CommonLogic
from cli.ui.menu import Menu


log = logging.getLogger(__name__)


class Upload(CommonLogic, Menu):

    def __init__(self, helpers):
        self.unpack_helpers(helpers)
        header = u'Upload'
        message = (u'Make sure updates are in "new" folder '
                   'then press "1" to start.')

        options = self.make_plugin_options()
        super(Upload, self).__init__(header, options, message)

    def make_plugin_options(self):
        plugin_options = []

        self.mgr = ExtensionManager(u'pyiu.uploaders')
        plugin_names = self.mgr.names()
        log.debug(u'Plugin names: {}'.format(plugin_names))

        for pgn in plugin_names:
            # passing none as a place holder for logic in
            # cli.ui.menu for processing of plugin menu creation
            # Logic will pass this to else since its len is
            # more then 2
            log.debug(u'Plugin name: {}'.format(pgn))
            option = (pgn, self.upload, None)
            plugin_options.append(option)
        plugin_options.append((u'Main Menu', self.done))

        return plugin_options

    def upload(self, name):
        # Load plugin & invoke upload method
        self.uploader.set_uploader(name)
        self.display_menu_header(u'{} Uploader'.format(name))
        try:
            self.uploader.upload()
            time.sleep(3)
        except Exception as e:
            msg = (u'Looks like you forgot to add USERNAME, PASSWORD '
                   'and/or REMOTE_DIR')
            self.display_msg(msg)
            log.debug(str(e), exc_info=True)
            input()
