import os
import sys

from nose import with_setup
from nose.tools import raises

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyi_updater.archiver import main, ArchiverError


class MyOpts(object):
    def __init__(self, name, version, archiver='zip', args=[]):
        self.name = name
        self.version_num = version
        self.archiver = archiver
        self.args = ['app']
        for i in args:
            self.args.append(i)


def setup_func():
    with open('mac', 'w') as f:
        f.write('temp test file')


def teardown_func():
    if os.path.exists('mac'):
        os.remove('mac')
    if os.path.exists('jms-mac-0.0.1.zip'):
        os.remove('jms-mac-0.0.1.zip')
    if os.path.exists('jms-mac-0.0.2.tar.gz'):
        os.remove('jms-mac-0.0.2.tar.gz')


def test_options_no_file():
    my_opts = MyOpts('jms', '0.0.1')
    assert main(my_opts) is False


@with_setup(setup_func, teardown_func)
def test_options_files():
    my_opts = MyOpts('jms', '0.0.2',
                     archiver='gzip', args=['mac', 'win', 'arm'])
    assert main(my_opts) is True
    assert os.path.exists('jms-mac-0.0.2.tar.gz') is True


@raises(ArchiverError)
def test_options_bad_name():
    my_opts = MyOpts('jms', '0.0.1', args=['mac', 'win', 'arm'])
    del my_opts.name
    if hasattr(my_opts, 'name'):
        delattr(my_opts, 'name')
    main(my_opts)


@raises(ArchiverError)
def test_options_bad_version():
    my_opts = MyOpts('jms', '0.0', args=['mac', 'win', 'arm'])
    main(my_opts)


@raises(ArchiverError)
def test_options_bad_platform():
    my_opts = MyOpts('jms', '0.0', args=['macaroni'])
    main(my_opts)
