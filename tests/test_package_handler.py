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
from pyi_updater.config import PyiUpdaterConfig
from pyi_updater.package_handler import PackageHandler

from tconfig import TConfig


def test_setup():
    updater = PyiUpdaterConfig()
    myconfig = TConfig()
    updater.update_config(myconfig)
    ph = PackageHandler(updater)


def test_setup_no_patches():
    updater = PyiUpdaterConfig()
    myconfig = TConfig()
    myconfig.UPDATE_PATCHES = False
    updater.update_config(myconfig)
    ph = PackageHandler(updater)
