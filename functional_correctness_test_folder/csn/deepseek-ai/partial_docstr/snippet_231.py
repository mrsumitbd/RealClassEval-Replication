
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
        self._bytes = bytearray(bytes)
        if len(self._bytes) % 2 != 0:
            self._bytes = self._bytes[:-1]

    def __getitem__(self, key):
        '''Returns the words in this wordarray at the given Python slice
        or word at the given integer index.'''
        if isinstance(key, int):
            if key < 0:
                key += len(self)
            if key < 0 or key >= len(self):
                raise IndexError("WordArray index out of range")
            byte_index = key * 2
            return (self._bytes[byte_index] << 8) | self._bytes[byte_index + 1]
        elif isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            return [self[i] for i in range(start, stop, step)]
        else:
            raise TypeError("Invalid argument type")

    def __len__(self):
        '''Returns the number of words in the WordArray.'''
        return len(self._bytes) // 2
