
import struct


class Array:
    '''Use a Struct as a callable to unpack a bunch of bytes as a list.'''

    def __init__(self, fmt):
        self.struct = struct.Struct(fmt)

    def __call__(self, buf):
        '''Perform the actual unpacking.'''
        return list(self.struct.iter_unpack(buf))
