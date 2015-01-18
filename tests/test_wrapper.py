import pytest

from pyi_updater.wrapper.options import (make_parser,
                                         make_subparser,
                                         add_build_parser,
                                         add_clean_parser,
                                         add_init_parser,
                                         add_keys_parser,
                                         add_log_parser,
                                         add_package_parser,
                                         add_upload_parser,
                                         add_version_parser)


@pytest.fixture
def parser():
    parser = make_parser()
    return parser


def test_build_no_options(parser):
    subparser = make_subparser(parser)
    add_build_parser(subparser)
    with pytest.raises(SystemExit):
        parser.parse_args([u'build'])


def test_build_no_appanme(parser):
    subparser = make_subparser(parser)
    add_build_parser(subparser)
    with pytest.raises(SystemExit):
        parser.parse_args([u'build', u'--app-version=0.2.10'])


def test_build_no_appversion(parser):
    subparser = make_subparser(parser)
    add_build_parser(subparser)
    with pytest.raises(SystemExit):
        parser.parse_args([u'build', u'--app-name=Test'])


def test_clean(parser):
    subparser = make_subparser(parser)
    add_build_parser(subparser)
    with pytest.raises(SystemExit):
        parser.parse_args([u'clean'])


def test_init(parser):
    subparser = make_subparser(parser)
    add_build_parser(subparser)
    with pytest.raises(SystemExit):
        parser.parse_args([u'init'])


def test_keys(parser):
    subparser = make_subparser(parser)
    add_build_parser(subparser)
    with pytest.raises(SystemExit):
        parser.parse_args([u'keys'])


def test_log(parser):
    subparser = make_subparser(parser)
    add_build_parser(subparser)
    with pytest.raises(SystemExit):
        parser.parse_args([u'log'])


def test_package(parser):
    subparser = make_subparser(parser)
    add_build_parser(subparser)
    with pytest.raises(SystemExit):
        parser.parse_args([u'pkg'])


def test_upload(parser):
    subparser = make_subparser(parser)
    add_build_parser(subparser)
    with pytest.raises(SystemExit):
        parser.parse_args([u'upload'])


def test_version(parser):
    subparser = make_subparser(parser)
    add_build_parser(subparser)
    with pytest.raises(SystemExit):
        parser.parse_args([u'version'])
