
class BufferSegment:
    '''Represents a segment within a ``BufferWithSegments``.
    This type is essentially a reference to N bytes within a
    ``BufferWithSegments``.
    The object conforms to the buffer protocol.
    '''

    def __init__(self, parent_buffer, offset, length):
        self._parent_buffer = parent_buffer
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
        return bytes(self._parent_buffer[self._offset:self._offset + self._length])
