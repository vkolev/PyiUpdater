import logging
import os
import re

from pyi_updater.exceptions import UtilsError
from pyi_updater.utils import (get_package_hashes,
                               parse_platform,
                               get_version_number,
                               )

log = logging.getLogger(__name__)


class Patch(object):

    def __init__(self, patch_info):
        self.dst_path = patch_info.get(u'dst')
        self.patch_name = patch_info.get(u'patch_name')
        self.dst_filename = patch_info.get(u'package')
        self.ready = self._check_attrs()

    def _check_attrs(self):
        if self.dst_path is not None:
            if not os.path.exists(self.dst_path):
                return False
        else:
            return False
        if self.patch_name is None:
            return False
        if self.dst_filename is None:
            return False
        return True


class Package(object):

    def __init__(self, file_):
        self.name = None
        self.version = None
        self.filename = file_
        self.version_path = None
        self.file_hash = None
        self.platform = None
        self.info = {'status': False, 'reason': ''}
        self.patch_info = {}
        # seems to produce the best diffs.
        # Tests on homepage: https://github.com/JohnyMoSwag/PyiUpdater
        # Zip doesn't keep +x permissions. Only using gz for now.
        # self.supported_extensions = [u'.zip', u'.gz']
        self.supported_extensions[u'.gz']
        self.extract_info(file_)

    def extract_info(self, package):
        """Gets version number, platform & hash for package.

        Args:
            package (str): filename
        """
        if os.path.splitext(package)[1].lower() not in \
                self.supported_extensions:
            msg = u'Not a supported archive format: {}'.format(package)
            self.info['reason'] = msg
            log.error(msg)
            return

        try:
            self.version = get_version_number(package)
        except UtilsError:
            msg = u'Package version not formatted correctly'
            self.info[u'reason'] = msg
            log.error(msg)
            return

        try:
            self.platform = parse_platform(package)
        except UtilsError:
            msg = u'Package platform not formatted correctly'
            self.info[u'reason'] = msg
            log.error(msg)
            return

        # No need to get any more info if above failed
        self.name = self._get_package_name(package)
        self.file_hash = get_package_hashes(package)
        self.info[u'status'] = True

    def _get_package_name(self, package):
        name = self._remove_version_number(package)
        name = self._remove_ext(name)
        name = self._remove_platform(name)
        return name

    def _remove_ext(self, filename):
        # Removes file ext from filename.
        data = os.path.splitext(filename)
        while len(data[1]) > 0:
            data = os.path.splitext(data[0])
        return data[0]

    def _remove_version_number(self, package_name):
        # Returns string with version number removed
        # What, thought it did something else? lol j/k
        reg = u'-[0-9]+\.[0-9]+\.[0-9]+'
        return re.sub(reg, '', package_name)

    def _remove_platform(self, name):
        name = re.sub(u'-[a-zA-Z0-9]{3,5}', '', name)
        return name
