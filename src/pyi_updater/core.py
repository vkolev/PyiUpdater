from pyi_updater.key_handler import KeyHandler
from pyi_updater.package_handler import PackageHandler
from pyi_updater.uploader import Uploader


class Core(object):

    def __init__(self, config=None):
        if config is not None:
            self.init(config)

    def init(self, config):
        self.kh = KeyHandler(config)
        self.ph = PackageHandler(config)
        self.up = Uploader(config)

    def setup(self):
        self.ph.setup()

    def process_packages(self):
        self.ph.process_packages()

    def set_uploader(self, requested_uploader):
        self.up.set_uploader(requested_uploader)

    def upload(self):
        self.up.upload()

    def make_keys(self):
        self.kh.make_keys()

    def sign_update(self):
        self.kh.sign_update()

    def get_public_key(self):
        self.kh.get_public_key()

    def copy_decrypted_private_key(self):
        self.kh.copy_decrypted_private_key()

    def print_public_key(self):
        self.kh.print_public_key()
