import time


def get_build():
    total = ''
    a = time.localtime(time.time())
    # total += str(a.tm_year)[2:]
    total += str(a.tm_mon)
    total += str(a.tm_mday)
    total += str(a.tm_hour)
    total += str(a.tm_min)
    return total

VERSION = (0, 13, 0, u'dev', get_build())
# VERSION = (0, 13, 0)


def _get_version(v):
    version = '{}.{}'.format(v[0], v[1])
    if v[2]:
        version = '{}.{}'.format(version, v[2])
    if len(v) >= 4 and v[3]:
        version = '{}-{}'.format(version, v[3])
        if v[3] == 'dev' and len(v) >= 5 and v[4] > 0:
            version = '{}{}'.format(version, v[4])
    return version


def get_version():
    return _get_version(VERSION)