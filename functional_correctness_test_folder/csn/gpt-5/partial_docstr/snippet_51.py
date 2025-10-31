import struct


class Array:
    '''Use a Struct as a callable to unpack a bunch of bytes as a list.'''

    def __init__(self, fmt):
        self._struct = struct.Struct(fmt)
        # Determine number of items produced per unpack
        self._items_per = len(self._struct.unpack(b'\x00' * self._struct.size))

    def __call__(self, buf):
        '''Perform the actual unpacking.'''
        mv = memoryview(buf)
        if len(mv) % self._struct.size != 0:
            raise ValueError(
                "Buffer size must be a multiple of the struct size")
        out = []
        for i in range(0, len(mv), self._struct.size):
            chunk = mv[i:i + self._struct.size]
            vals = self._struct.unpack(chunk)
            if self._items_per == 1:
                out.append(vals[0])
            else:
                out.append(vals)
        return out
