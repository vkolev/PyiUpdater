import json
import logging
import os
import shutil

from jms_utils.paths import ChDir

log = logging.getLogger(__name__)


def count_contents(d):
    with ChDir(d):
        count = len(os.listdir(os.getcwd()))
    return count


def migrate(data_dir):
    info = {}
    p_dir = os.path.dirname(data_dir)
    log.debug('Parent directory: {}'.format(p_dir))
    config_dir = os.path.join(p_dir, u'.pyiupdater')
    config_file = os.path.join(config_dir, u'data.json')
    if not os.path.exists(config_dir):
        os.mkdir(config_dir)
    if os.path.exists(config_file):
        with open(config_file, u'r') as f:
            try:
                info = json.loads(f.read())
            except ValueError:
                log.debug("Could not load config file")
    files_dir = os.path.join(data_dir, u'files')
    info['boot_strap'] = 100
    with open(config_file, u'w') as f:
        f.write(json.dumps(info, indent=2, sort_keys=True))
    # Moving files to be removed
    old_dir = os.path.join(data_dir, u'safe-to-remove')
    shutil.move(files_dir, old_dir)
    if os.path.exists(files_dir):
        shutil.rmtree(files_dir, ignore_errors=True)
    os.makedirs(files_dir)
