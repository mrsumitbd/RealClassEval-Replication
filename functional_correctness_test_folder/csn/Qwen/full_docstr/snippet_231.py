
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
        self._words = [int.from_bytes(bytes[i:i+2], byteorder='big')
                       for i in range(0, len(bytes), 2)]

    def __getitem__(self, key):
        '''Returns the words in this wordarray at the given Python slice
        or word at the given integer index.'''
        return self._words[key]

    def __len__(self):
        '''Returns the number of words in this wordarray.'''
        return len(self._words)
