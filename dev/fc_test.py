import logging
import not_so_tuf.filecrypt as fc


s = logging.StreamHandler()

log = logging.getLogger('')
log.setLevel(logging.DEBUG)
log.addHandler(s)


PASSWORD = 'This is my password.'
FILENAME = 'test.txt'
ENC_FILENAME = FILENAME + '.enc'
dec_hash = 'f4c657756a3f47d2cf1f0108d3a61108'
enc_hash = '20548d68080f4174a29a73d9bea88e9a'


def make_test_file(filename):
    log.info('Creating test file.')
    with open(filename, 'w') as f:
        f.write('This is just a test. Do not be alarmed.' * 1000)


def main():
    global FILENAME
    global ENC_FILENAME
    global PASSWORD
    make_test_file(FILENAME)
    raw_input('\n\nCheck the created test file')
    n = fc.NewCrypt(FILENAME)
    n.encrypt()
    n.password = None
    raw_input('\n\nGo look at your results.')
    n.decrypt()

main()
