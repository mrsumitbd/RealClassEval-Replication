
class BufferSegment:
    '''Represents a segment within a ``BufferWithSegments``.
    This type is essentially a reference to N bytes within a
    ``BufferWithSegments``.
    The object conforms to the buffer protocol.
    '''

    def __init__(self, buffer, offset, length):
        self._buffer = buffer
        self._offset = offset
        self._length = length

    @property
    def offset(self):
        '''The byte offset of this segment within its parent buffer.'''
        return self._offset

    def __len__(self):
        '''Obtain the length of the segment, in bytes.'''
        return self._length

    def tobytes(self):
        '''Obtain bytes copy of this segment.'''
        return self._buffer[self._offset:self._offset + self._length]

    def __getitem__(self, index):
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            return self.tobytes()[start:stop:step]
        if index < 0:
            index += len(self)
        if index < 0 or index >= len(self):
            raise IndexError("index out of range")
        return self.tobytes()[index]

    def __bytes__(self):
        return self.tobytes()
