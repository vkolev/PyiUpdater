from nose.tools import *
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyi_updater.utils import rsa_verify

signature = '84e402a13281b299352ddb1844f61d542d11641da1cc30e3837e6b5cdad0fe9e779a1a9dbcd0d9463947d0de63b329b02456c67beba97ea5275cd1385ca15b2fb822218ee45c279c81024a2ecf37ce594fef0c58a0a67799d0105644476a0dc0fdbc391f4257d043b870b1aa5cfa0149d43036ebc65933c2016db3ac74ecfc8e'
# signature = hexlify(rsa.pkcs1.sign(b'bella', priv, 'SHA-256'))
key = (0xa6480f4d0d057c9290a2f755354b6fc1689b7667f414ca432984da211c3cdf367c3e6ded82da9528657c336b454b2ee57301ff14e2ecbba0a8e91d006032acc029696a9eb70d41737df25ef47b166b61a9fcad1cb8f73662130cc7c02d2a10006d69d5aed31742dbe66b7819d5f98e9b6b35a83811918f74517e965b23cd73df, 65537)
# key = (pub.n, pub.e)

if sys.version_info[0] == 2:
    @raises(AssertionError)
    def test_rsa_py2():
        assert(repr(rsa_verify('bella', signature, key))) # True
        assert(repr(rsa_verify('brutta', signature, key))) # False
        assert(repr(rsa_verify('bella', signature[2:], key))) # False
        assert(repr(rsa_verify('bella', signature, (key[0]+1, key[1])))) # False
        assert(repr(rsa_verify('bella', signature, (key[0], key[1]+1)))) # False
        assert(repr(rsa_verify('bella'.decode(), signature, key))) # AssertionError
    test_rsa_py2()

elif sys.version_info[0] == 3:
    @raises(AssertionError)
    def test_rsa_py3():
        assert(repr(rsa_verify('bella'.encode('latin1'), signature, key))) # True
        assert(repr(rsa_verify('brutta'.encode('latin1'), signature, key))) # False
        assert(repr(rsa_verify('bella'.encode('latin1'), signature[2:], key))) # False
        assert(repr(rsa_verify('bella'.encode('latin1'), signature, (key[0]+1, key[1])))) # False
        assert(repr(rsa_verify('bella'.encode('latin1'), signature, (key[0], key[1]+1)))) # False
        assert(repr(rsa_verify('bella', signature, key))) # AssertionError
    test_rsa_py3
