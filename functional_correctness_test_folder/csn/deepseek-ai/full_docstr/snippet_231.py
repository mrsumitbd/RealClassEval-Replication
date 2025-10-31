
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
        self._bytes = bytes[:len(bytes) - (len(bytes) % 2)]
        self._words = []
        for i in range(0, len(self._bytes), 2):
            word = (self._bytes[i] << 8) | self._bytes[i+1]
            self._words.append(word)

    def __getitem__(self, key):
        '''Returns the words in this wordarray at the given Python slice
        or word at the given integer index.'''
        if isinstance(key, slice):
            return self._words[key]
        else:
            return self._words[key]

    def __len__(self):
        '''Returns the number of words in this wordarray.'''
        return len(self._words)
