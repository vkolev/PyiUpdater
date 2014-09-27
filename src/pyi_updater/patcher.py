import bz2
import logging
import os
import sys

from blinker import signal
try:
    import bsdiff4
except ImportError:
    bsdiff4 = None
from jms_utils.paths import ChDir
from jms_utils.system import get_system
from six import BytesIO

from pyi_updater.downloader import FileDownloader
from pyi_updater.exceptions import PatcherError
from pyi_updater.utils import (get_package_hashes,
                               StarAccessDict,
                               version_string_to_tuple,
                               version_tuple_to_string)

log = logging.getLogger(__name__)

platform_ = get_system()

progress_signal = signal(u'progress_info')


class Patcher(object):
    """Downloads, verifies, and patches binaries

    Args:
        name (str): Name of binary to patch

        json_data (dict): Info dict with all package meta data

        current_version (str): Version number of currently installed binary

        highest_version (str): Newest version available

        update_folder (str): Path to update folder to place updated binary in
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get(u'name', None)
        self.json_data = kwargs.get(u'json_data', None)
        self.star_access_update_data = StarAccessDict(self.json_data)
        self.current_version = kwargs.get(u'current_version', None)
        self.highest_version = kwargs.get(u'highest_version', None)
        self.update_folder = kwargs.get(u'update_folder', None)
        self.update_url = kwargs.get(u'update_url', None)
        self.verify = kwargs.get(u'verify', True)
        self.patch_data = []
        self.patch_binary_data = []
        self.og_binary = None
        # ToDo: Update tests with linux archives.
        # Used for testing.
        self.plat = kwargs.get(u'platform', platform_)
        self.current_filename = kwargs.get(u'current_filename', None)
        self.current_file_hash = kwargs.get(u'current_file_hash', None)

        file_info = self._current_file_info(self.name,
                                            self.current_version)
        if self.current_filename is None:
            self.current_filename = file_info['filename']
        if self.current_file_hash is None:
            self.current_file_hash = file_info['file_hash']

    def start(self):
        "Starts patching process"

        log.debug(u'Starting patch updater...')
        # Check hash on installed binary to begin patching
        binary_check = self._verify_installed_binary()
        if not binary_check:
            log.warning(u'Binary check failed...')
            return False
        # Getting all required patch meta-data
        all_patches = self._get_all_patches(self.name)
        if all_patches is False:
            log.warning(u'Cannot find all patches...')
            return False

        # Download and verify patches in 1 go
        download_check = self._download_verify_patches()
        if download_check is False:
            log.warning(u'Patch check failed...')
            return False

        try:
            self._apply_patches_in_memory()
        except PatcherError:
            return False
        else:
            try:
                self._write_update_to_disk()
            except PatcherError:
                return False

        return True

    def _verify_installed_binary(self):
        # Verifies currently installed binary against known hash
        log.debug(u'Checking for current installed binary to patch')

        # I just really like using this ChDir context
        # manager.  Even sent the developer a cup of coffee
        with ChDir(self.update_folder):
            if not os.path.exists(self.current_filename):
                log.warning(u'Cannot find binary to patch')
                return False

            installed_file_hash = get_package_hashes(self.current_filename)
            if self.current_file_hash != installed_file_hash:
                log.warning(u'Binary hash mismatch')
                return False
            with open(self.current_filename, u'rb') as f:
                self.og_binary = f.read()
            os.remove(self.current_filename)
        log.debug(u'Binary found and verified')
        return True

    # We will take all versions.  Then append any version
    # thats greater then the current version to the list
    # of needed patches.
    def _get_all_patches(self, name):
        needed_patches = []
        versions = []
        try:
            u_versions = map(version_string_to_tuple,
                             self.json_data[u'updates'][name].keys())
            versions.extend(u_versions)
        except KeyError:
            log.debug(u'No updates found in updates dict')

        # Sorted here because i may forget to leave it when i delete
        # the list/set down below.
        # How i envisioned it: sorted(list(set(needed_patches)))
        versions = sorted(versions)
        log.debug(u'getting required patches')
        for i in versions:
            if i > version_string_to_tuple(self.current_version):
                needed_patches.append(i)

        # Taking the list of needed patches and extracting the
        # patch data from it. If any loop fails, will return False
        # and start full binary update.
        log.debug(u'Getting patch meta-data')

        # Used to guarantee patches are only added once
        needed_patches = list(set(needed_patches))

        for p in needed_patches:
            info = {}
            v_num = version_tuple_to_string(p)
            plat_key = '{}*{}*{}*{}'.format(u'updates', name,
                                            v_num, self.plat)
            plat_info = self.star_access_update_data.get(plat_key)

            try:
                info[u'patch_name'] = plat_info[u'patch_name']
                info[u'patch_url'] = self.update_url + plat_info[u'patch_name']
                info[u'patch_hash'] = plat_info[u'patch_hash']
                self.patch_data.append(info)
            except KeyError:
                log.error(u'Missing required patch meta-data')
                return False
        return True

    def _download_verify_patches(self):
        # Downloads & verifies all patches
        log.debug('Downloading patches')
        total = 0
        if len(self.patch_data) > 3:
            percent_each = 100 / len(self.patch_data)
        else:
            percent_each = None
        for p in self.patch_data:
            fd = FileDownloader(p[u'patch_name'], p[u'patch_url'],
                                p[u'patch_hash'], self.verify)

            data = fd.download_verify_return()
            if data is not None:
                self.patch_binary_data.append(data)
                # Gathering info to send in signal
                if percent_each is not None:
                    total += percent_each
                    done = total
                else:
                    done = '...'
                progress_signal.send(info=u'Downloading patches',
                                     percent=str(done))
            else:
                progress_signal.send(info=u'Failed to download patches',
                                     percent=u'...')
                return False
        progress_signal.send(info=u'Download Complete', percent=u'100')
        return True

    def _apply_patches_in_memory(self):
        # Applies a sequence of patches in memory
        log.debug(u'Applying patches')
        # Beginning the patch process
        self.new_binary = self.og_binary
        progress_signal.send(info=u'Applying Patches')
        for i in self.patch_binary_data:
            try:
                self.new_binary = bsdiff4.patch(self.new_binary, i)
            except Exception as err:
                progress_signal.send(info=u'Failed to apply patches')
                log.debug(err, exc_info=True)
                log.error(err)
                raise PatcherError(u'Patch failed to apply')

    def _write_update_to_disk(self):
        # Writes updated binary to disk
        log.debug('Writing update to disk')

        filename_key = '{}*{}*{}*{}*{}'.format(u'updates', self.name,
                                               self.highest_version, self.plat,
                                               u'filename')

        filename = self.star_access_update_data.get(filename_key)
        if filename is None:
            raise PatcherError('Filename missing in version file')

        with ChDir(self.update_folder):
            try:
                with open(filename, u'wb') as f:
                    f.write(self.new_binary)
            except IOError:
                # Removes file is it somehow got created
                if os.path.exists(filename):
                    os.remove(filename)
                log.error(u'Failed to open file for writing')
                raise PatcherError(u'Failed to open file for writing')
            else:
                if self.current_file_hash != get_package_hashes(filename):
                    os.remove(filename)
                    raise PatcherError(u'Patched file hash bad checksum')

    def _current_file_info(self, name, version):
        # Returns filename and hash for given name and version
        info = {}
        plat_key = '{}*{}*{}*{}'.format(u'updates', name,
                                        version, self.plat)
        plat_info = self.star_access_update_data.get(plat_key)

        try:
            filename = plat_info[u'filename']
        except Exception as err:
            log.debug(str(err))
            filename = ''
        info[u'filename'] = filename

        try:
            file_hash = plat_info[u'file_hash']
        except Exception as err:
            log.debug(str(err))
            file_hash = ''
        info[u'file_hash'] = file_hash
        return info


class bsdiff4_py(object):
    """Pure-python version of bsdiff4 module that can only patch, not diff.

    By providing a pure-python fallback, we don't force frozen apps to
    bundle the bsdiff module in order to make use of patches.  Besides,
    the patch-applying algorithm is very simple.
    """
    @staticmethod
    def patch(source, patch):
        #  Read the length headers
        l_bcontrol = _decode_offt(patch[8:16])
        l_bdiff = _decode_offt(patch[16:24])
        l_target = _decode_offt(patch[24:32])
        #  Read the three data blocks
        e_bcontrol = 32 + l_bcontrol
        e_bdiff = e_bcontrol + l_bdiff
        bcontrol = bz2.decompress(patch[32:e_bcontrol])
        bdiff = bz2.decompress(patch[e_bcontrol:e_bdiff])
        bextra = bz2.decompress(patch[e_bdiff:])
        #  Decode the control tuples
        tcontrol = []
        for i in xrange(0, len(bcontrol), 24):
            tcontrol.append((
                _decode_offt(bcontrol[i:i+8]),
                _decode_offt(bcontrol[i+8:i+16]),
                _decode_offt(bcontrol[i+16:i+24]),
            ))
        #  Actually do the patching.
        #  This is the bdiff4 patch algorithm in slow, pure python.
        source = BytesIO(source)
        result = BytesIO()
        bdiff = BytesIO(bdiff)
        bextra = BytesIO(bextra)
        for (x, y, z) in tcontrol:
            diff_data = bdiff.read(x)
            orig_data = source.read(x)
            if sys.version_info[0] < 3:
                for i in xrange(len(diff_data)):
                    result.write(chr((ord(diff_data[i]) +
                                 ord(orig_data[i])) % 256))
            else:
                for i in xrange(len(diff_data)):
                    result.write(bytes([(diff_data[i] + orig_data[i]) % 256]))
            result.write(bextra.read(y))
            source.seek(z, os.SEEK_CUR)
        return result.getvalue()

# I think this was placed here because
# i was getting errors when it was at the top
# of the file.
if bsdiff4 is None:
    bsdiff4 = bsdiff4_py


def _decode_offt(bytes):
    """Decode an off_t value from a string.

    This decodes a signed integer into 8 bytes.  I'd prefer some sort of
    signed vint representation, but this is the format used by bsdiff4.
    """
    if sys.version_info[0] < 3:
        bytes = map(ord, bytes)
    x = bytes[7] & 0x7F
    for b in xrange(6, -1, -1):
        x = x * 256 + bytes[b]
    if bytes[7] & 0x80:
        x = -x
    return x
