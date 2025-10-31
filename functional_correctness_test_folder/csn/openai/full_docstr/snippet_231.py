
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
        if not isinstance(bytes, (bytes, bytearray)):
            raise TypeError("WordArray requires a bytes-like object")
        self._bytes = bytes
        self._len = len(bytes) // 2  # ignore last byte if odd

    def __len__(self):
        '''Returns the number of words in this wordarray.'''
        return self._len

    def _word_at(self, i):
        if i < 0:
            i += self._len
        if i < 0 or i >= self._len:
            raise IndexError("WordArray index out of range")
        b0 = self._bytes[2 * i]
        b1 = self._bytes[2 * i + 1]
        return (b0 << 8) | b1

    def __getitem__(self, key):
        '''Returns the words in this wordarray at the given Python slice
        or word at the given integer index.'''
        if isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            return [self._word_at(i) for i in range(start, stop, step)]
        elif isinstance(key, int):
            return self._word_at(key)
        else:
            raise TypeError("WordArray indices must be integers or slices")
