from nose.tools import with_setup
import os

from jms_utils.paths import ChDir

from pyi_updater.downloader import FileDownloader


FILENAME = u'dont+delete+nst+test.txt'
FILENAME_WITH_SPACES = 'dont delete nst test.txt'
FILE_HASH = u'9da856b0b8b77c838d6945e0bfbc62fff978a9dd5256eed231fc499b5d4b183c'
URL = u'https://s3-us-west-1.amazonaws.com/not-so-tuf/'


def teardown_func():
    with ChDir(u'tests'):
        if os.path.exists(FILENAME):
            os.remove(FILENAME)


@with_setup(None, teardown_func)
def test_download_write():
    with ChDir(u'tests'):
        fd = FileDownloader(FILENAME, URL, FILE_HASH)
        success = fd.download_verify_write()
        assert success is True


@with_setup(None, teardown_func)
def test_download_write_bad_hash():
    with ChDir(u'tests'):
        fd = FileDownloader(FILENAME, URL, u'38839didkdkflrlrkdfa')
        success = fd.download_verify_write()
        assert success is False


def test_download_return():
    with ChDir(u'tests'):
        fd = FileDownloader(FILENAME, URL, FILE_HASH)
        binary_data = fd.download_verify_return()
        assert binary_data is not None


def test_download_return_fail():
    with ChDir(u'tests'):
        fd = FileDownloader(FILENAME, URL, u'JKFEIFJILEFJ983NKFNKL')
        binary_data = fd.download_verify_return()
        assert binary_data is None


def test_url_with_spaces():
    with ChDir(u'tests'):
        fd = FileDownloader(FILENAME_WITH_SPACES, URL, FILE_HASH)
        binary_data = fd.download_verify_return()
        assert binary_data is not None


def test_bad_url():
    with ChDir('tests'):
        fd = FileDownloader(FILENAME, u'bad url', u'bad hash')
        binary_data = fd.download_verify_return()
        assert binary_data is None


def test_bad_content_length():
    with ChDir(u'tests'):
        class FakeHeaders(object):
            headers = {}
        fd = FileDownloader(FILENAME, URL, FILE_HASH)
        data = FakeHeaders()
        assert fd._get_content_length(data) == 100000


@with_setup(None, teardown_func)
def test_good_conent_length():
    with ChDir(u'tests'):
        fd = FileDownloader(FILENAME, URL, FILE_HASH)
        fd.download_verify_write()
        assert fd.content_length == 60000
