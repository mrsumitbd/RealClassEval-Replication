
import struct


class Array:
    '''Use a Struct as a callable to unpack a bunch of bytes as a list.'''

    def __init__(self, fmt):
        '''Initialize the Struct unpacker.'''
        self._struct = struct.Struct(fmt)

    def __call__(self, buf):
        '''Perform the actual unpacking.'''
        return list(self._struct.unpack(buf))
