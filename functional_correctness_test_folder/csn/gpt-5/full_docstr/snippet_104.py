class BufferSegment:
    '''Represents a segment within a ``BufferWithSegments``.
    This type is essentially a reference to N bytes within a
    ``BufferWithSegments``.
    The object conforms to the buffer protocol.
    '''

    def __init__(self, buffer, offset=0, length=None):
        mv = memoryview(buffer)
        if mv.ndim != 1:
            mv = mv.cast('B')
        if offset < 0:
            raise ValueError("offset must be non-negative")
        total_len = mv.nbytes
        if length is None:
            length = total_len - offset
        if length < 0:
            raise ValueError("length must be non-negative")
        end = offset + length
        if end > total_len:
            raise ValueError("offset + length exceeds buffer size")
        self._parent_view = mv
        self._offset = int(offset)
        # Slice in bytes; memoryview slicing is by elements (1 byte here)
        self._view = mv[self._offset:end]

    @property
    def offset(self):
        '''The byte offset of this segment within its parent buffer.'''
        return self._offset

    def __len__(self):
        '''Obtain the length of the segment, in bytes.'''
        return self._view.nbytes

    def tobytes(self):
        '''Obtain bytes copy of this segment.'''
        return self._view.tobytes()

    # Optional conveniences
    def __bytes__(self):
        return self.tobytes()

    def __repr__(self):
        return f"{self.__class__.__name__}(len={len(self)}, offset={self.offset})"

    def __getitem__(self, key):
        return self._view[key]
