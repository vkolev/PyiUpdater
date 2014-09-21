import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__name__))))

from pyi_updater.key_handler import KeyHandler
from pyi_updater.utils import rsa_verify


def test_signature():
    pub_key_file = os.path.join(u'tests', u'test data', u'nst.pub')
    version_file = os.path.join(u'tests', u'test data', u'version.json')
    with open(version_file, u'r') as f:
        version_data = json.loads(f.read())

    sig = version_data[u'sig']
    del version_data[u'sig']
    version_data = json.dumps(version_data, sort_keys=True)

    with open(pub_key_file, u'r') as pkf:
        public_key = KeyHandler._pub_key_string_to_tuple(pkf.read())

    assert rsa_verify(version_data, sig, public_key) is True
