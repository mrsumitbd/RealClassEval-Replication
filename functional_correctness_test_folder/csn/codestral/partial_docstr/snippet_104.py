
class BufferSegment:

    def __init__(self, buffer, offset, length):
        self._buffer = buffer
        self._offset = offset
        self._length = length

    @property
    def offset(self):
        return self._offset

    def __len__(self):
        return self._length

    def tobytes(self):
        '''Obtain bytes copy of this segment.'''
        return bytes(self._buffer[self._offset:self._offset + self._length])
