import json
import logging
import os
import shutil


log = logging.getLogger(__name__)


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
    # We are going to get the number of folders
    # in each app or lib name. We will use this number
    # as a number to boot strap the patch number during
    # package processing.
    boot_strap = 1
    files_dir = os.path.join(data_dir, u'files')
    files = os.listdir(files_dir)
    for f in files:
        # The number of versions for each app
        if os.path.isdir(os.path.join(data_dir, f)) is False:
            continue
        num = len(os.listdir(os.path.join(data_dir, f)))
        if num > boot_strap:
            boot_strap = num
    info['boot_strap'] = boot_strap
    with open(config_file, u'w') as f:
        f.write(json.dumps(info, indent=2, sort_keys=True))
    # Moving files to be removed
    old_dir = os.path.join(data_dir, u'safe-to-remove')
    shutil.move(files_dir, old_dir)
    if os.path.exists(files_dir):
        shutil.move(files_dir)
    os.makedirs(files_dir)
