from io import BytesIO
import logging
import time
import sys

from blinker import signal
import requests

from pyi_updater.exceptions import FileDownloaderError
from pyi_updater.utils import get_hash

log = logging.getLogger(__name__)


progress_signal = signal(u'progress_info')


class FileDownloader(object):
    """The FileDownloader object downloads files to memory and
    verifies their hash.  If hash is verified data is either
    written to disk to returned to calling object

    Args:

        filename (str): The name of file to download

        url (str): The url to retrieve the file

        hexdigest str(str): The hash checksum of the file to download
    """
    def __init__(self, filename, url, hexdigest, verify=True):
        self.start = time.time()
        self.filename = filename
        self.url = url
        self.hexdigest = hexdigest
        self.verify = verify
        self.b_size = 4096 * 4
        self.file_binary_data = None

    def download_verify_write(self):
        """Downloads file then verifies against provided hash
        If hash verfies then writes data to disk

        Returns:
            (bool) Meanings::

                True - Hash verified

                False - Hash not verified
        """
        self._download_to_memory()
        check = self._check_hash()
        if check:
            log.debug(u'File hash verified')
            self._write_to_file()
            progress_signal.send(info=u'Download Successful')
            return True
        else:
            log.debug(u'Cannot verify file hash')
            del self.file_binary_data
            del self.my_file
            progress_signal.send(info=u'Download Failed')
            return False

    def download_verify_return(self):
        """
        Downloads file to memory, checks against provided hash
        If matched returns binary data

        Returns:
            (data) Meanings::

                Data - If everything verified

                None - If any verification didn't pass
        """
        self._download_to_memory()
        check = self._check_hash()
        if check:
            log.debug(u'File hash verified')
            return self.file_binary_data
        else:
            log.debug(u'Cannot verify file hash')
            return None

    @staticmethod
    def _best_block_size(elapsed_time, bytes):
        # Returns best block size for current internet connection speed
        new_min = max(bytes / 2.0, 1.0)
        new_max = min(max(bytes * 2.0, 1.0), 4194304)  # Do not surpass 4 MB
        if elapsed_time < 0.001:
            return int(new_max)
        rate = bytes / elapsed_time
        if rate > new_max:
            return int(new_max)
        if rate < new_min:
            return int(new_min)
        return int(rate)

    def _download_to_memory(self):
        # Downloads file to memory.  Keeps internal reference
        try:
            data = requests.get(self.url, verify=self.verify, stream=True)
        except requests.exceptions.HTTPError:
            log.debug(u'Might have had spaces in an S3 url...')
            self.url = self.url.replace(' ', '+')
            data = None
            log.debug(u'S3 updated url {}'.format(self.url))
        except requests.exceptions.SSLError:
            log.error(u'SSL cert not verified')
            raise FileDownloaderError(u'SSL cert not verified')
        except Exception as e:
            # Catch whatever else comes up and log it
            # to help fix other http related issues
            log.error(str(e), exc_info=True)
            return None

        if data is None:
            # Let's try one more time with the fixed url
            try:
                data = requests.get(self.url, verify=self.verify, stream=True)
            except requests.exceptions.SSLError:
                log.error(u'SSL cert not verified')
                raise FileDownloaderError(u'SSL cert not verified')
            except Exception as e:
                log.error(str(e), exc_info=True)
                self.file_binary_data = None
                return None

        self.content_length = self._get_content_length(data)
        self.my_file = BytesIO()
        log.debug(u'Downloading {} from \n{}'.format(self.filename, self.url))
        recieved_data = 0

        start_block = None
        for block in data.iter_content(self.b_size):
            end_block = time.time()
            if start_block is not None:
                self.b_size = self._best_block_size(end_block - start_block,
                                                    len(block))
                log.debug(u'Block size: %s' % self.b_size)
            self.my_file.write(block)
            recieved_data += len(block)
            percent = self._calc_progress_percent(recieved_data,
                                                  self.content_length)
            progress_signal.send(info=u'Downloading', percent=percent)
            sys.stdout.write(u'\r{} Percent Complete'.format(percent))
            sys.stdout.flush()
            start_block = time.time()

        sys.stdout.write('\n')
        sys.stdout.flush()
        self.my_file.flush()
        self.my_file.seek(0)
        self.file_binary_data = self.my_file.read()
        progress_signal.send(info=u'Download Complete', percent=u'100')
        log.debug(u'Download Complete')
        log.debug(u'Finished in {} seconds'.format(time.time() -
                  self.start))

    def _write_to_file(self):
        # Writes download data in memory to disk
        with open(self.filename, u'wb') as f:
            f.write(self.file_binary_data)

    def _check_hash(self):
        # Checks hash of downloaded file
        if self.file_binary_data is None:
            return False
        log.debug(u'Checking file hash')
        log.debug(u'Update hash: {}'.format(self.hexdigest))

        file_hash = get_hash(self.file_binary_data)
        if file_hash == self.hexdigest:
            return True
        return False

    def _get_content_length(self, data):
        content_length = int(data.headers.get(u"Content-Length", 100000))
        log.debug(u'Got content length of: %s', content_length)
        return content_length

    @staticmethod
    def _calc_eta(start, now, total, current):
        # Not currently implemented
        # Calculates remaining time of download
        if total is None:
            return u'--:--'
        dif = now - start
        if current == 0 or dif < 0.001:  # One millisecond
            return u'--:--'
        rate = float(current) / dif
        eta = int((float(total) - float(current)) / rate)
        (eta_mins, eta_secs) = divmod(eta, 60)
        if eta_mins > 99:
            return u'--:--'
        return u'%02d:%02d' % (eta_mins, eta_secs)

    def _calc_progress_percent(self, x, y):
        percent = float(x) / y * 100
        percent = u'%.1f' % percent
        return percent
