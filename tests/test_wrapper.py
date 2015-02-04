# --------------------------------------------------------------------------
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
# --------------------------------------------------------------------------
import pytest

from pyi_updater.wrapper.options import (make_parser,
                                         make_subparser,
                                         add_build_parser,
                                         add_clean_parser,
                                         add_init_parser,
                                         add_keys_parser,
                                         add_log_parser,
                                         add_make_spec_parser,
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
    add_clean_parser(subparser)
    assert parser.parse_args([u'clean'])


def test_init(parser):
    subparser = make_subparser(parser)
    add_init_parser(subparser)
    assert parser.parse_args([u'init'])


def test_keys(parser):
    subparser = make_subparser(parser)
    add_keys_parser(subparser)
    assert parser.parse_args([u'keys'])


def test_log(parser):
    subparser = make_subparser(parser)
    add_log_parser(subparser)
    assert parser.parse_args([u'log'])


def test_make_spec(parser):
    subparser = make_subparser(parser)
    add_make_spec_parser(subparser)
    assert parser.parse_args([u'make-spec'])


def test_package(parser):
    subparser = make_subparser(parser)
    add_package_parser(subparser)
    assert parser.parse_args([u'pkg'])


def test_upload(parser):
    subparser = make_subparser(parser)
    add_upload_parser(subparser)
    assert parser.parse_args([u'upload'])


def test_version(parser):
    subparser = make_subparser(parser)
    add_version_parser(subparser)
    assert parser.parse_args([u'version'])
