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
        mv = memoryview(bytes_)
        even_len = (len(mv) // 2) * 2
        self._view = mv[:even_len]

    def __getitem__(self, key):
        '''Returns the words in this wordarray at the given Python slice
        or word at the given integer index.'''
        n = len(self)
        if isinstance(key, slice):
            indices = range(n)[key]
            return [self[i] for i in indices]
        # integer index
        idx = key
        if idx < 0:
            idx += n
        if idx < 0 or idx >= n:
            raise IndexError('WordArray index out of range')
        off = idx * 2
        hi = self._view[off]
        lo = self._view[off + 1]
        return (hi << 8) | lo

    def __len__(self):
        '''Returns the number of words in this wordarray.'''
        return len(self._view) // 2
