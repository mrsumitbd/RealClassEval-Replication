import struct
from functools import reduce
import binascii

class Member:

    def __init__(self, hunk):
        info = parse_hunk(hunk)
        info['filename'] = info['path']
        info['size'] = int(info['size'])
        info['packed_size'] = int(info['packed_size'] or '0')
        info['block'] = int(info['block'] or '0')
        if info['crc']:
            info['crc'] = reduce(lambda x, y: x * 256 + y, struct.unpack('BBBB', binascii.unhexlify(info['crc'])), 0)
        self.__dict__.update(info)

    def isfile(self):
        return self.attributes[0] != 'D'

    def isdir(self):
        return self.attributes[0] == 'D'