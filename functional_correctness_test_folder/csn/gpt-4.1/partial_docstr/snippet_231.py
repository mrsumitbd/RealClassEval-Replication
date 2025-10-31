
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
        if not isinstance(bytes_, (bytes, bytearray)):
            raise TypeError("Input must be bytes or bytearray")
        self._bytes = bytes_[:len(bytes_) & ~1]  # ignore last byte if odd

    def __getitem__(self, key):
        '''Returns the words in this wordarray at the given Python slice
        or word at the given integer index.'''
        nwords = len(self)
        if isinstance(key, int):
            if key < 0:
                key += nwords
            if key < 0 or key >= nwords:
                raise IndexError("WordArray index out of range")
            i = key * 2
            return (self._bytes[i] << 8) | self._bytes[i+1]
        elif isinstance(key, slice):
            indices = range(*key.indices(nwords))
            return [self[i] for i in indices]
        else:
            raise TypeError("Invalid argument type")

    def __len__(self):
        return len(self._bytes) // 2
