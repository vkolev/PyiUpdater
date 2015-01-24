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


import gzip
import logging
import os
import StringIO

from pyi_updater.utils import lazy_import

six = None

log = logging.getLogger(__name__)


def get_mac_dot_app_dir(directory):
    """Returns parent directory of mac .app

    Args:

       directory (str): Current directory

    Returns:

       (str): Parent directory of mac .app
    """
    return os.path.dirname(os.path.dirname(os.path.dirname(directory)))


def get_highest_version(name, plat, easy_data):
    """Parses version file and returns the highest version number.

    Args:

       name (str): name of file to search for updates

       easy_data (dict): data file to search

    Returns:

       (str) Highest version number
    """
    version_key = u'{}*{}*{}'.format(u'latest', name, plat)
    version = easy_data.get(version_key)

    if version is not None:
        log.debug(u'Highest version: {}'.format(version))
    else:
        log.error(u'No updates for "{}" on {} exists'.format(name, plat))
    return version


def get_filename(name, version, platform, easy_data):
        """Gets full filename for given name & version combo

        Args:

           name (str): name of file to get full filename for

           version (str): version of file to get full filename for

           easy_data (dict): data file to search

        Returns:

           (str) Filename with extension
        """
        filename_key = u'{}*{}*{}*{}*{}'.format(u'updates', name, version,
                                                platform, u'filename')
        filename = easy_data.get(filename_key)

        log.debug(u"Filename for {}-{}: {}".format(name, version, filename))
        return filename


def convert_to_list(data, default=None):
    global six
    if six is None:
        six = lazy_import(u'six')
    if isinstance(data, list):
        return data
    if isinstance(data, tuple):
        return list(data)
    if isinstance(data, six.string_types):
        return [data]
    else:
        log.debug('Not of string of tuple')
        return default


def gzip_decompress(data):
    compressed_file = StringIO.StringIO()
    compressed_file.write(data)
    #
    # Set the file's current position to the beginning
    # of the file so that gzip.GzipFile can read
    # its contents from the top.
    #
    compressed_file.seek(0)

    decompressed_file = gzip.GzipFile(fileobj=compressed_file, mode='rb')
    data = decompressed_file.read()
    compressed_file.close()
    decompressed_file.close()
    return data
