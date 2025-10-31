
class WordArray:
    '''WordArrays are somewhat analogous to Python bytearrays, but
    currently much more limited in functionality.  They provide a
    readonly view of a bytearray addressable and iterable as a sequence
    of 16-bit words.  This is convenient for telemetry processing as
    packets are often more naturally addressable on word, as opposed to
    byte, boundaries.
    '''

    def __init__(self, bytes_):
        '''Creates a new wordarray from the given bytearray.
        The given bytearray should contain an even number of bytes.  If
        odd, the last byte is ignored.
        '''
        # Accepts bytes, bytearray, or any buffer protocol object
        self._bytes = bytes(bytes_)
        # Ignore last byte if odd length
        if len(self._bytes) % 2 != 0:
            self._bytes = self._bytes[:-1]
        self._nwords = len(self._bytes) // 2

    def __getitem__(self, key):
        '''Returns the words in this wordarray at the given Python slice
        or word at the given integer index.'''
        if isinstance(key, int):
            if key < 0:
                key += self._nwords
            if key < 0 or key >= self._nwords:
                raise IndexError("WordArray index out of range")
            i = key * 2
            return (self._bytes[i] << 8) | self._bytes[i+1]
        elif isinstance(key, slice):
            indices = range(*key.indices(self._nwords))
            return [self[i] for i in indices]
        else:
            raise TypeError("WordArray indices must be integers or slices")

    def __len__(self):
        '''Returns the number of words in this wordarray.'''
        return self._nwords
