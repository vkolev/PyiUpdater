import logging
import time

log = logging.getLogger(__name__)


class BaseUploader(object):
    """Base Uploader.  All uploaders should subclass
    this base class
    """
    def __init__(self):
        self.failed_uploads = []
        self.deploy_dir = None

    def init(self, **Kwargs):
        """Used to initialize your plugin with username,
        password, file list, remote_dir/bucket & host.
        self._connect should be called after you grab all the
        info you need.

        Kwargs:

            file_list (list): List of files to upload

            host (str): Either ip or domain name of remote servers

            bucket_name/remote_dir (str): Remote location for update

            remote_dir (str): The directory on remote server to upload files to

            username/aws_access_id (str): login for service

            password/ssh_key_file/aws_secret_key (str): login for service
        """
        raise NotImplementedError(u'Must be implemented in subclass.')

    def upload(self):
        """Uploads all files in file_list"""
        self.files_completed = 1
        self.file_count = self._get_filelist_count()
        for f in self.file_list:
            msg = u'\n\nUploading: {}' .format(f)
            msg2 = u' - File {} of {}\n'.format(self.files_completed,
                                                self.file_count)
            print(msg + msg2)
            complete = self._upload_file(f)
            if complete:
                log.debug('{} uploaded successfully'.format(f))
                self.files_completed += 1
            else:
                log.debug(u'{} failed to upload.  will retry'.format(f))
                self.failed_uploads.append(f)
        if len(self.failed_uploads) > 0:
            self._retry_upload()
        if len(self.failed_uploads) < 1:
            print(u"\nUpload Complete")
            time.sleep(3)
            return True
        else:
            print(u'The following files were not uploaded')
            for i in self.failed_uploads:
                log.error(u'{} failed to upload'.format(i))
                print(i)
            return False

    def _retry_upload(self):
        # Takes list of failed downloads and tries to re upload them
        retry = self.failed_uploads[:]
        self.failed_uploads = []
        failed_count = len(retry)
        count = 1
        for f in retry:
            msg = u'\n\nRetyring: {} - File {} of {}\n'.format(f,
                                                               count,
                                                               failed_count)
            print(msg)
            complete = self._upload_file(f)
            if complete:
                log.debug(u'{} uploaded on retry'.format(f))
                count += 1
            else:
                self.failed_uploads.append(f)
        if len(self.failed_uploads) >= 1:
            print(u'\nThe following files failed to upload...')
            for f in self.failed_uploads:
                print(f)
            time.sleep(3)
            return False
        else:
            print('\nUpload complete')
            return True

    def _connect(self):
        # Connects client attribute to service
        raise NotImplementedError(u'Must be implemented in subclass.')

    def _upload_file(self, filename):
        # """Uploads file to remote repository

        # Args:
        #     filename (str): file to upload

        # Returns:
        #     (bool) Meaning::

        #         True - Upload Successful

        #         False - Upload Failed
        # """
        raise NotImplementedError('Must be implemented in subclass.')

    def _get_filelist_count(self):
        return len(self.file_list)
