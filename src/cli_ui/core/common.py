class CommonLogic(object):

    def unpack_helpers(self, helpers):
        self.file_crypt = helpers[u'file_crypt']
        self.package_handler = helpers[u'package_handler']
        self.key_handler = helpers[u'key_handler']
        self.uploader = helpers[u'uploader']
        self.config = helpers[u'config']
        self.save = helpers[u'save']

    def update_helpers(self):
        self.package_handler.init_app(self.config)
        self.key_handler.init_app(self.config)
        self.uploader.init_app(self.config)

    def done(self):
        pass
