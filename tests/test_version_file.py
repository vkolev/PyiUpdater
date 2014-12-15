import json
import os

import ed25519


def test_signature():
    pub_key_file = os.path.join(u'tests', u'test data', u'jms.pub')
    version_file = os.path.join(u'tests', u'test data', u'version.json')
    with open(version_file, u'r') as f:
        version_data = json.loads(f.read())

    sig = version_data[u'sig']
    del version_data[u'sig']
    version_data = json.dumps(version_data, sort_keys=True)

    with open(pub_key_file, u'r') as pkf:
        public_key = ed25519.VerifyingKey(pkf.read(), encoding='base64')

    public_key.verify(sig, version_data, encoding='base64')
