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
        if not isinstance(bytes_, (bytes, bytearray, memoryview)):
            raise TypeError("bytes must be a bytes-like object")
        mv = memoryview(bytes_)
        # Cast to bytes for immutability/read-only behavior
        self._bytes = bytes(mv.tobytes())
        self._nwords = len(self._bytes) // 2  # ignore last odd byte if present

    def __getitem__(self, key):
        '''Returns the words in this wordarray at the given Python slice
        or word at the given integer index.'''
        if isinstance(key, slice):
            indices = range(*key.indices(len(self)))
            return [self[i] for i in indices]
        # integer index
        n = len(self)
        if key < 0:
            key += n
        if key < 0 or key >= n:
            raise IndexError("WordArray index out of range")
        i = key * 2
        b1 = self._bytes[i]
        b2 = self._bytes[i + 1]
        return (b1 << 8) | b2  # big-endian 16-bit word

    def __len__(self):
        return self._nwords
