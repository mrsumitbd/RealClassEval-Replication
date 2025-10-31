
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
        # Ensure we have a bytes-like object and drop the last byte if odd
        if len(bytes_) % 2:
            bytes_ = bytes_[:-1]
        # Store as immutable bytes for safety
        self._bytes = bytes(bytes_)

    def __len__(self):
        return len(self._bytes) // 2

    def __getitem__(self, key):
        '''Returns the words in this wordarray at the given Python slice
        or word at the given integer index.'''
        nwords = len(self)
        if isinstance(key, int):
            # Handle negative indices
            if key < 0:
                key += nwords
            if key < 0 or key >= nwords:
                raise IndexError('WordArray index out of range')
            i = key * 2
            return (self._bytes[i] << 8) | self._bytes[i + 1]
        elif isinstance(key, slice):
            start, stop, step = key.indices(nwords)
            # Build list of words for the slice
            result = []
            for idx in range(start, stop, step):
                i = idx * 2
                result.append((self._bytes[i] << 8) | self._bytes[i + 1])
            return result
        else:
            raise TypeError('WordArray indices must be integers or slices')

    def __iter__(self):
        '''Iterate over the words in the array.'''
        for i in range(len(self)):
            yield self[i]

    def __repr__(self):
        return f'{self.__class__.__name__}({list(self)!r})'
