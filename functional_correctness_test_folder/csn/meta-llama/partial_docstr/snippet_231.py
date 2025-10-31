
class WordArray:
    '''WordArrays are somewhat analogous to Python bytearrays, but
    currently much more limited in functionality.  They provide a
    readonly view of a bytearray addressable and iterable as a sequence
    of 16-bit words.  This is convenient for telemetry processing as
    packets are often more naturally addressable on word, as opposed to
    byte, boundaries.
    '''

    def __init__(self, bytes):
        '''Creates a new wordarray from the given bytearray.
        The given bytearray should contain an even number of bytes.  If
        odd, the last byte is ignored.
        '''
        if len(bytes) % 2 != 0:
            bytes = bytes[:-1]
        self.bytes = bytes

    def __getitem__(self, key):
        '''Returns the words in this wordarray at the given Python slice
        or word at the given integer index.'''
        if isinstance(key, int):
            if key < 0:
                key += len(self) // 2
            if key < 0 or key >= len(self) // 2:
                raise IndexError("WordArray index out of range")
            return (self.bytes[key*2] << 8) | self.bytes[key*2 + 1]
        elif isinstance(key, slice):
            start, stop, step = key.indices(len(self) // 2)
            return [(self.bytes[i*2] << 8) | self.bytes[i*2 + 1] for i in range(start, stop, step)]
        else:
            raise TypeError("WordArray indices must be integers or slices")

    def __len__(self):
        return len(self.bytes)
