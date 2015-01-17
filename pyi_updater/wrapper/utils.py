import logging
import os
import re
import subprocess
import sys
import time

from pyi_updater import settings

log = logging.getLogger(__name__)

fix = u"""
found = []
for d in a.datas:
    if d[0] in found:
        a.datas.remove(d)
    else:
        found.append(d[0])
"""


def check_repo():
    if not os.path.exists(settings.CONFIG_DATA_FOLDER):
        log.debug('Not a PyiUpdater repo')
        sys.exit('Not a PyiUpdater repo: Must init first.')


def check_version(version):
    match = re.match(u'(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)',
                     version)
    if match is None:
        log.debug('Version did not match')
        return False
    else:
        log.debug('Version matched')
        return True


def pretty_time(sec):
    return time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime(sec))


def run(cmd):
    log.debug(u'Command: {}'.format(cmd))
    exit_code = subprocess.call(cmd)
    return exit_code
