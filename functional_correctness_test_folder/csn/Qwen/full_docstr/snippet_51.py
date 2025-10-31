
import struct


class Array:
    '''Use a Struct as a callable to unpack a bunch of bytes as a list.'''

    def __init__(self, fmt):
        '''Initialize the Struct unpacker.'''
        self.fmt = fmt
        self.size = struct.calcsize(fmt)

    def __call__(self, buf):
        '''Perform the actual unpacking.'''
        if len(buf) % self.size != 0:
            raise ValueError(
                "Buffer size is not a multiple of the format size")
        return list(struct.unpack(self.fmt * (len(buf) // self.size), buf))
