import logging
import os

log = logging.getLogger(__name__)


def get_mac_dot_app_dir(dir_):
    return os.path.dirname(os.path.dirname(os.path.dirname(dir_)))


def get_highest_version(name, plat, easy_data):
    # Parses version file and returns the highest version number.
    #
    # Args:
    #    name (str): name of file to search for updates
    #
    # Returns:
    #    (str) Highest version number
    version_key = u'{}*{}*{}'.format(u'latest', name, plat)

    version = easy_data.get(version_key)

    if version is not None:
        log.debug(u'Highest version: {}'.format(version))
    else:
        log.error(u'No updates named "{}" exists'.format(name))
    return version
