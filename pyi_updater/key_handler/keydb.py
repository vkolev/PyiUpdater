import json
import logging
import os
import time


log = logging.getLogger(__name__)


class KeyDB(object):

    def __init__(self, data_dir, load=False):
        self.data_dir = data_dir
        self.key_file = os.path.join(self.data_dir, 'key.db')
        self.data = None
        if load is True:
            self.load()

    def add_key(self, public, private, key_type='ed25519'):
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
        return self._get_keys(u'public')

    def get_private_keys(self):
        return self._get_keys(u'private')

    def _get_keys(self, key):
        keys = []
        for k, v in self.data.items():
            if v[u'revoked'] is False:
                keys.append(v[key])
        return keys

    def get_revoked_key(self):
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
        with open(self.key_file, u'w') as f:
            f.write(json.dumps(self.data, indent=True, sort_keys=True))
        log.debug(u'Wrote key.db to disk')
