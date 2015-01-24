#--------------------------------------------------------------------------
# Copyright 2014 Digital Sapphire Development Team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#--------------------------------------------------------------------------


import logging
import os
import sys

from pyi_updater.exceptions import UploaderError
from pyi_updater import settings
from pyi_updater.utils import (lazy_import,
                               remove_dot_files)

log = logging.getLogger(__name__)

stevedore = None
ns = settings.UPLOAD_PLUGIN_NAMESPACE


class Uploader(object):
    """Uploads updates to configured servers.  SSH, SFTP, S3
    Will automatically pick the correct uploader depending on
    what is configured thorough the config object

    Sets up client with config values from obj

        Args:

            obj (instance): config object
    """
    def __init__(self, app=None):
        global stevedore
        stevedore = lazy_import(u'stevedore')
        if app:
            self.init_app(app)

    def init_app(self, obj):
        """Sets up client with config values from obj

        Args:

            obj (instance): config object
        """
        data_dir = os.path.abspath(os.getcwd())
        self.data_dir = os.path.join(data_dir, settings.USER_DATA_FOLDER)
        self.deploy_dir = os.path.join(self.data_dir, u'deploy')
        self.remote_dir = obj.get(u'REMOTE_DIR')
        self.host = obj.get(u'HOST')
        self.username = obj.get(u'USERNAME')
        # If password is none get ssh key path
        self.password = obj.get(u'PASSWORD')
        self.uploader = None
        self.test = False

        # Extension Manager
        self.mgr = stevedore.extension.ExtensionManager(namespace=ns)

    def upload(self):
        """Proxy function that calls the upload method on the received uploader
        Only calls the upload method if an uploader is set.
        """
        if self.uploader is not None:  # pragma: no cover
            self.uploader.deploy_dir = self.deploy_dir
            try:
                self.uploader.upload()
            except Exception as err:
                log.debug(str(err), exc_info=True)
                sys.exit(str(err))
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
        files = os.listdir(self.deploy_dir)
        files = remove_dot_files(files)  # pragma: no cover
        self.uploader.init(username=self.username,
                           password=self.password,
                           remote_dir=self.remote_dir,
                           host=self.host,
                           files=files)  # pragma: no cover
