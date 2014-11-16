from __future__ import print_function

import os
import shutil
import sys

from jms_utils.paths import ChDir


HTML_DIR = os.path.abspath(os.path.join(u'_build', u'html'))
DEST_DIR = os.path.join(os.path.expanduser(u'~'), u'Dropbox',
                        u'Web Sites', u'RW6')


def main():
    if len(sys.argv) < 2:
        sys.exit(u'Must pass "rel" or "dev" as arg')

    arg = sys.argv[1].lower()
    if arg == u'dev':
        path = os.path.join(DEST_DIR, u'PyiUpdater-Dev')
    elif arg == u'rel':
        path = os.path.join(DEST_DIR, u'PyiUpdater')
    else:
        sys.exit(u'Invalid argument')

    with ChDir(path):
        files = os.listdir(os.getcwd())
        for f in files:
            if f.startswith(u'.'):
                continue
            elif f in [u'objects.inv', u'composer.json',
                       u'index.php', u'Procfile']:
                continue
            elif os.path.isfile(f):
                os.remove(f)
            elif os.path.isdir(f):
                shutil.rmtree(f, ignore_errors=True)

    with ChDir(HTML_DIR):
        files = os.listdir(os.getcwd())
        for f in files:
            if f.startswith(u'.'):
                continue
            if f == u'index.html':
                os.rename(u'index.html', u'home.html')
                shutil.copy(u'home.html', path)
            if os.path.isfile(f):
                shutil.copy(f, os.path.join(path, f))
            elif os.path.isdir(f):
                shutil.copytree(f, path + os.sep + f)

if __name__ == '__main__':
    main()
    print(u'Move complete')
