class CommonLogic(object):

    def unpack_helpers(self, helpers):
        self.file_crypt = helpers[u'file_crypt']
        self.pyiu = helpers[u'pyiu']
        self.config = helpers[u'config']
        self.save = helpers[u'save']
