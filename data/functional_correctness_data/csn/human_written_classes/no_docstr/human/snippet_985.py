from functools import reduce
import binascii
import struct

class Member:

    def __init__(self, info):
        info['filename'] = info.pop('name')
        info['size'] = int(info.get('size', 0))
        info['packed_size'] = int(info.get('packed_size', 0))
        info['ratio'] = float(info.get('ratio', '0%')[:-1]) / 100
        info['crc32'] = reduce(lambda x, y: x * 256 + y, struct.unpack('BBBB', binascii.unhexlify(info['crc32'])), 0)
        self.__dict__.update(info)

    def isfile(self):
        return self.type == 'File'

    def isdir(self):
        return self.type == 'Directory'