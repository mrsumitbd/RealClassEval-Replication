
class BufferSegment:
    def __init__(self, buffer, offset=0, length=None):
        if not isinstance(buffer, (bytes, bytearray, memoryview)):
            raise TypeError("buffer must be bytes-like object")
        self._buffer = memoryview(buffer)
        self._offset = offset
        if length is None:
            length = len(self._buffer) - offset
        if offset < 0 or length < 0 or offset + length > len(self._buffer):
            raise ValueError("Invalid offset or length")
        self._length = length

    @property
    def offset(self):
        return self._offset

    def __len__(self):
        return self._length

    def tobytes(self):
        '''Obtain bytes copy of this segment.'''
        return self._buffer[self._offset:self._offset + self._length].tobytes()
