import sys
import traceback


class STDError(Exception):
    """Extends exceptions to show added message if error isn't expected.

    Args:

        msg (str): error message

    Kwargs:

        tb (obj): is the original traceback so that it can be printed.

        expected (bool): Meaning:

                            True - Report issue msg not shown

                            False - Report issue msg shown
    """
    def __init__(self, msg, tb=None, expected=False):
        if not expected:
            msg = msg + (u'; please report this issue on https://github.com'
                         '/JohnyMoSwag/PyiUpdater/issues')
        super(Exception, self).__init__(msg)

        self.traceback = tb
        self.exc_info = sys.exc_info()  # preserve original exception

    def format_traceback(self):
        if self.traceback is None:
            return None
        return u''.join(traceback.format_tb(self.traceback))


class ArchiverError(STDError):
    """Raised for Client exceptions"""
    def __init__(self, *args, **kwargs):
        super(ArchiverError, self).__init__(*args, **kwargs)


class ClientError(STDError):
    """Raised for Client exceptions"""
    def __init__(self, *args, **kwargs):
        super(ClientError, self).__init__(*args, **kwargs)


class ConfigError(STDError):
    """Raised for Config exceptions"""
    def __init__(self, *args, **kwargs):
        super(ConfigError, self).__init__(*args, **kwargs)


class FileDownloaderError(STDError):
    """Raised for File Downloader exceptions"""
    def __init__(self, *args, **kwargs):
        super(FileDownloaderError, self).__init__(*args, **kwargs)


class KeyHandlerError(STDError):
    """Raised for Key Handler exceptions"""
    def __init__(self, *args, **kwargs):
        super(KeyHandlerError, self).__init__(*args, **kwargs)


class PackageError(STDError):
    """Raised for Package Handler exceptions"""
    def __init__(self, *args, **kwargs):
        super(PackageError, self).__init__(*args, **kwargs)


class PackageHandlerError(STDError):
    """Raised for Package Handler exceptions"""
    def __init__(self, *args, **kwargs):
        super(PackageHandlerError, self).__init__(*args, **kwargs)


class PatcherError(STDError):
    """Raised for Patcher exceptions"""
    def __init__(self, *args, **kwargs):
        super(PatcherError, self).__init__(*args, **kwargs)


class PyiUpdaterError(STDError):
    """Raised for Framework exceptions"""
    def __init__(self, *args, **kwargs):
        super(PyiUpdaterError, self).__init__(*args, **kwargs)


class UpdaterError(STDError):
    """Raised for Updater exceptions"""
    def __init__(self, *args, **kwargs):
        super(UpdaterError, self).__init__(*args, **kwargs)


class UploaderError(STDError):
    """Raised for Uploader exceptions"""
    def __init__(self, *args, **kwargs):
        super(UploaderError, self).__init__(*args, **kwargs)


class UtilsError(STDError):
    """Raised for Uploader exceptions"""
    def __init__(self, *args, **kwargs):
        super(UtilsError, self).__init__(*args, **kwargs)
