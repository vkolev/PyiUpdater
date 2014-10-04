#!/usr/bin/env python

from __future__ import print_function
import logging
import os
import sys

from jms_utils.logger import log_format_string
from pyi_updater.utils import cwd_

log = logging.getLogger()
log.setLevel(logging.DEBUG)
fmt_str = log_format_string()
nh = logging.NullHandler()
nh.setLevel(logging.DEBUG)
log.addHandler(nh)

if os.path.exists(os.path.join(cwd_, u'pyi.log')):
    ch = logging.FileHandler(os.path.join(cwd_, u'pyi.log'))
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(fmt_str)
    log.addHandler(ch)


# Interface
from cli.core import Worker


def main():
    try:
        worker = Worker()
        worker.start()
    except KeyboardInterrupt:
        # ToDo: Add clean up stuff here
        sys.stdout.write(u'\n\nExited by user\n')
        sys.stdout.flush()
        sys.exit(0)
    except Exception as e:
        print(str(e))
        log.error(str(e), exc_info=True)
