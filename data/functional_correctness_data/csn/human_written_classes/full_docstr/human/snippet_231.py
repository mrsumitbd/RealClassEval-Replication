class WordArray:
    """WordArrays are somewhat analogous to Python bytearrays, but
    currently much more limited in functionality.  They provide a
    readonly view of a bytearray addressable and iterable as a sequence
    of 16-bit words.  This is convenient for telemetry processing as
    packets are often more naturally addressable on word, as opposed to
    byte, boundaries.
    """
    __slots__ = ['_bytes']

    def __init__(self, bytes):
        """Creates a new wordarray from the given bytearray.

        The given bytearray should contain an even number of bytes.  If
        odd, the last byte is ignored.
        """
        self._bytes = bytes

    def __getitem__(self, key):
        """Returns the words in this wordarray at the given Python slice
        or word at the given integer index."""
        length = len(self)
        if isinstance(key, slice):
            return [self[n] for n in range(*key.indices(length))]
        elif isinstance(key, int):
            if key < 0:
                key += length
            if key >= length:
                msg = 'wordarray index (%d) is out of range [0 %d].'
                raise IndexError(msg % (key, length - 1))
            index = 2 * key
            return self._bytes[index] << 8 | self._bytes[index + 1]
        else:
            raise TypeError('wordarray indices must be integers.')

    def __len__(self):
        """Returns the number of words in this wordarray."""
        return len(self._bytes) / 2