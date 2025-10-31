import struct


class Array:
    '''Use a Struct as a callable to unpack a bunch of bytes as a list.'''

    def __init__(self, fmt):
        self._struct = struct.Struct(fmt)

    def __call__(self, buf):
        '''Perform the actual unpacking.'''
        size = self._struct.size
        if len(buf) % size != 0:
            raise struct.error("Buffer size is not a multiple of struct size")
        return [self._struct.unpack(buf[i:i+size]) for i in range(0, len(buf), size)]
