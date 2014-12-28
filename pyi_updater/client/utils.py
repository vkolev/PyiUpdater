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

log = logging.getLogger(__name__)


def get_mac_dot_app_dir(dir_):
    """Returns parent directory of mac .app

    Args:

       dir_ (str): Current directory

    Returns:

       (str): Parent directory of mac .app
    """
    return os.path.dirname(os.path.dirname(os.path.dirname(dir_)))


def get_highest_version(name, plat, easy_data):
    """Parses version file and returns the highest version number.

    Args:

       name (str): name of file to search for updates

       easy_data (dict): data file to search

    Returns:

       (str) Highest version number
    """
    log.debug('Data:\n{}'.format(easy_data))
    version_key = u'{}*{}*{}'.format(u'latest', name, plat)

    version = easy_data.get(version_key)

    if version is not None:
        log.debug(u'Highest version: {}'.format(version))
    else:
        log.error(u'No updates named "{}" exists'.format(name))
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
        log.debug('Data:\n{}'.format(easy_data))
        filename_key = u'{}*{}*{}*{}*{}'.format(u'updates', name, version,
                                                platform, u'filename')
        filename = easy_data.get(filename_key)

        log.debug(u"Filename for {}-{}: {}".format(name, version, filename))
        return filename
