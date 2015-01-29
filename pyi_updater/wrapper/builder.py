# --------------------------------------------------------------------------
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
# --------------------------------------------------------------------------
import logging
import os
import shutil
import sys
import time

from jms_utils.paths import ChDir
from jms_utils.system import get_system

from pyi_updater import settings
from pyi_updater.hooks import get_hook_dir
from pyi_updater.utils import make_archive
from pyi_updater.utils import (check_repo,
                               check_version,
                               run)

log = logging.getLogger(__name__)


class Builder(object):

    def __init__(self, args, pyi_args):
        check_repo()
        self.args = args
        self.pyi_args = pyi_args

    def build(self):
        start = time.time()
        temp_name = get_system()
        app_info = self._check_input_file(self.pyi_args)
        self._setup()
        if app_info[u'type'] == u'spec':
            self._build(self.args, app_info[u'name'])
        else:
            self.spec_file_path = os.path.join(self.spec_dir,
                                               temp_name + u'.spec')
            self._make_spec(self.args, self.pyi_args, temp_name, app_info)
            self._build(self.args)
        self._archive(self.args, temp_name)
        finished = time.time() - start
        log.info(u'Build finished in {:.2f} seconds.'.format(finished))

    def make_spec(self):
        temp_name = get_system()
        app_info = self._check_input_file(self.pyi_args)
        self._make_spec(self.args, self.pyi_args, temp_name, app_info,
                        spec_only=True)

    def _setup(self):
        self.pyi_dir = os.path.join(os.getcwd(), settings.USER_DATA_FOLDER)
        self.new_dir = os.path.join(self.pyi_dir, u'new')
        self.build_dir = os.path.join(os.getcwd(), settings.CONFIG_DATA_FOLDER)
        self.spec_dir = os.path.join(self.build_dir, u'spec')
        self.work_dir = os.path.join(self.build_dir, u'work')
        for d in [self.build_dir, self.spec_dir, self.work_dir,
                  self.pyi_dir, self.new_dir]:
            if not os.path.exists(d):
                log.debug(u'Creating directory: {}'.format(d))
                os.mkdir(d)

    def _check_input_file(self, pyi_args):
        verified = False
        for p in pyi_args:
            if p.endswith(u'.py'):
                log.debug(u'Building from python source file: {}'.format(p))
                app_info = {u'type': u'script', u'name': p}
                verified = True
                break
            elif p.endswith(u'.spec'):
                log.debug(u'Building from spec file: {}'.format(p))
                app_info = {u'type': u'spec', u'name': p}
                verified = True
                break
        if verified is False:
            log.debug(u'No accepted files passed to builder')
            sys.exit(u'Must pass a python script or spec file')
        return app_info

    def _make_spec(self, args, pyi_args, temp_name, app_info, spec_only=False):
        log.debug('App Info: {}'.format(app_info))

        if args.console is True or args.nowindowed is True \
                or args._console is True:
            if u'-c' not in pyi_args:
                log.debug('Adding -c to pyi args')
                pyi_args.append(u'-c')
        if args.windowed is True or args.noconsole is True \
                or args._windowed is True:
            if u'-w' not in pyi_args:
                log.debug('Adding -w to pyi args')
                pyi_args.append(u'-w')
        pyi_args.append(u'-F')
        pyi_args.append(u'--name={}'.format(temp_name))
        if spec_only is True:
            log.debug('User generated spec file')
            pyi_args.append(u'--specpath={}'.format(os.getcwd()))
        else:
            pyi_args.append(u'--specpath={}'.format(self.spec_dir))
        pyi_args.append(u'--additional-hooks-dir={}'.format(get_hook_dir()))
        pyi_args.append(app_info[u'name'])

        cmd = ['pyi-makespec'] + pyi_args
        log.debug('Make spec cmd: {}'.format(' '.join([c for c in cmd])))
        exit_code = run(cmd)
        if exit_code != 0:
            log.error(u'Spec file creation failed with '
                      u'code: {}'.format(exit_code))
            sys.exit(1)
        else:
            log.info(u'Spec file created.')

    def _build(self, args, spec_file_path=None):
        if check_version(args.app_version) is False:
            sys.exit(u"""Error: version # needs to be in the form of "0.10.0"

        Visit url for more info:

            http://semver.org/
                      """)
        build_args = [u'pyinstaller']
        if args.clean is True:
            build_args.append(u'--clean')
        build_args.append(u'--distpath={}'.format(self.new_dir))
        build_args.append(u'--workpath={}'.format(self.work_dir))
        build_args.append(u'-y')
        if spec_file_path is None:
            build_args.append(self.spec_file_path)
        else:
            build_args.append(spec_file_path)

        log.debug('Build cmd: {}'.format(''.join([b for b in build_args])))
        exit_code = run(build_args)
        if exit_code != 0:
            log.error('Build failed with code: {}'.format(exit_code))
            sys.exit(1)
        else:
            log.info('Build successful')

    def _archive(self, args, temp_name):
        # Now archive the file
        with ChDir(self.new_dir):
            if os.path.exists(temp_name + u'.app'):
                log.debug(u'Got mac .app')
                app_name = temp_name + u'.app'
                name = args.app_name
            elif os.path.exists(temp_name + u'.exe'):
                log.debug(u'Got win .exe')
                app_name = temp_name + u'.exe'
                name = args.app_name
            else:
                app_name = temp_name
                name = args.app_name
            version = args.app_version
            log.debug('Temp Name: {}'.format(temp_name))
            log.debug(u'Appname: {}'.format(app_name))
            log.debug('Version: {}'.format(version))

            # Time for some archive creation!
            file_name = make_archive(name, version, app_name)
            log.debug(u'Archive name: {}'.format(file_name))
            if args.keep is False:
                if os.path.exists(temp_name):
                    log.debug('Removing: {}'.format(temp_name))
                    if os.path.isfile(temp_name):
                        os.remove(temp_name)
                    else:
                        shutil.rmtree(temp_name, ignore_errors=True)
                if os.path.exists(app_name):
                    log.debug('Removing: {}'.format(temp_name))
                    if os.path.isfile(app_name):
                        os.remove(app_name)
                    else:
                        shutil.rmtree(app_name, ignore_errors=True)
        log.info(u'{} has been placed in your new folder\n'.format(file_name))
