#--------------------------------------------------------------------------
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
#--------------------------------------------------------------------------


import json
import logging
import os
import time


log = logging.getLogger(__name__)


class KeyDB(object):
    u"""Handles finding, sorting, getting meta-data, moving packages.

    Kwargs:

        data_dir (str): Path to directory containing key.db

        load (bool):

            Meaning:

                True: Load db on initialization

                False: Do not load db on initialization
    """

    def __init__(self, data_dir, load=False):
        self.data_dir = data_dir
        self.key_file = os.path.join(self.data_dir, 'key.db')
        self.data = None
        if load is True:
            self.load()

    def add_key(self, public, private, key_type='ed25519'):
        u"""Adds key pair to database

        Args:

            public (str): Public key

            private (str): Private key

            key_type (str): The type of key pair. Default ed25519
        """
        _time = time.time()
        num = len(self.data) + 1
        data = {
            u'date': _time,
            u'public': public,
            u'private': private,
            u'revoked': False,
            u'key_type': key_type,
        }
        log.debug('Adding public key to db: {}'.format(public))
        self.data[num] = data
        self.save()

    def get_public_keys(self):
        u"Returns a list of all valid public keys"
        return self._get_keys(u'public')

    def get_private_keys(self):
        u"Returns a list of all valid private keys"
        return self._get_keys(u'private')

    def _get_keys(self, key):
        order = []
        keys = []
        for k, v in self.data.items():
            if v[u'revoked'] is False:
                order.append(int(k))
        order = sorted(order)
        for o in order:
            try:
                k = self.data[str(o)][key]
                keys.append(k)
            except KeyError:
                continue
        return keys

    def get_revoked_key(self):
        u"Returns most recent revoked key pair"
        keys = []
        for k, v in self.data.items():
            if v[u'revoked'] is True:
                keys.append(int(k))
        if len(keys) >= 1:
            key = sorted(keys)[-1]
            info = self.data[str(key)]
        else:
            info = None
        return info

    def revoke_key(self, count=1):
        u"""Revokes key pair

        Args:

            count (int): The number of keys to revoke. Oldest first
        """
        keys = map(str, self.data.keys())
        keys = sorted(keys)
        c = 0
        for k in keys:
            if c >= count:
                break
            if self.data[k][u'revoked'] is False:
                self.data[k][u'revoked'] = True
                c += 1
        self.save()

    def load(self):
        u"Loads data from key.db"
        log.debug(u'Loading key.db')
        self.data = dict()
        if os.path.exists(self.key_file):
            try:
                with open(self.key_file, u'r') as f:
                    self.data = json.loads(f.read())
                log.debug(u'Loaded key.db')
            except Exception as err:
                log.debug(u'Failed to load key.db')
                log.debug(str(err))
                log.debug('Created new key.db file')
        else:
            log.debug('Key.db file not found creating new')

    def save(self):
        u"Saves data to key.db"
        with open(self.key_file, u'w') as f:
            f.write(json.dumps(self.data, indent=True, sort_keys=True))
        log.debug(u'Wrote key.db to disk')
