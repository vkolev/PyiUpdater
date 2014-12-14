import logging
import os

from pyi_updater.exceptions import UploaderError
from pyi_updater.utils import (lazy_import,
                               remove_dot_files)

log = logging.getLogger(__name__)

stevedore = None


class Uploader(object):
    """Uploads updates to configured servers.  SSH, SFTP, S3
    Will automatically pick the correct uploader depending on
    what is configured thorough the config object

    Sets up client with config values from obj

        Args:
            obj (instance): config object
    """
    def __init__(self, app=None):
        stevedore = lazy_import(u'stevedore')
        global stevedore
        if app:
            self.init_app(app)

    def init_app(self, obj):
        """Sets up client with config values from obj

        Args:
            obj (instance): config object
        """
        self.data_dir = obj.get(u'DEV_DATA_DIR')
        if self.data_dir is not None:
            self.data_dir = os.path.join(self.data_dir, u'pyi-data')
            self.deploy_dir = os.path.join(self.data_dir, u'deploy')
        else:
            log.debug(u'DEV_DATA_DIR is None. Setup failed.')

        self.remote_dir = obj.get(u'REMOTE_DIR')
        self.host = obj.get(u'HOST', None)

        self.username = obj.get(u'USERNAME')

        # If password is none get ssh key path
        self.password = obj.get(u'PASSWORD')
        self.uploader = None
        self.test = False

        # Extension Manager
        self.mgr = stevedore.extension.ExtensionManager(namespace=u'pyiupdat'
                                                        'er.uploaders',)

    def upload(self):
        """Proxy function that calls the upload method on the received uploader
        Only calls the upload method if an uploader is set.
        """
        if self.uploader is not None:  # pragma: no cover
            self.uploader.deploy_dir = self.deploy_dir
            self.uploader.upload()
        else:
            raise UploaderError(u'Must call set_uploader first', expected=True)

    def set_uploader(self, requested_uploader):
        """Returns an uploader object. 1 of S3, SCP, SFTP.
        SFTP uploaders not supported at this time.

        Args:
            requested_uploader (string): Either s3 or scp

        Returns:
            object (instance): Uploader object
        """
        if isinstance(requested_uploader, str) is False:
            raise UploaderError(u'Must pass str to set_uploader',
                                expected=True)

        try:  # pragma: no cover
            plugin = self.mgr[requested_uploader]
        except Exception as err:  # pragma: no cover
            log.debug(u'EP CACHE: {}'.format(self.mgr.ENTRY_POINT_CACHE))
            log.error(str(err))
            raise UploaderError(u'Requested uploader is not installed',
                                expected=True)

        self.uploader = plugin.plugin()  # pragma: no cover
        msg = u'Requested uploader: {}'.format(requested_uploader)
        log.debug(msg)  # pragma: no cover

        files = remove_dot_files(os.listdir(self.deploy_dir))  # pragma: no cover
        self.uploader.init(username=self.username,
                           password=self.password,
                           remote_dir=self.remote_dir,
                           host=self.host,
                           files=files)  # pragma: no cover
