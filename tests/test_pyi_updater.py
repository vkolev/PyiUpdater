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
from pyi_updater import PyiUpdaterConfig

from tconfig import TConfig


def test_dev_dir_none():
    updater = PyiUpdaterConfig()
    myconfig = TConfig()
    myconfig.APP_NAME = None
    updater.update_config(myconfig)
    assert updater[u'APP_NAME'] == u'PyiUpdater App'
