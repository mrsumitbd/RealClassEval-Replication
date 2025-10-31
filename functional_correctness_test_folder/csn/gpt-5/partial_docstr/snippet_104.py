class BufferSegment:
    def __init__(self, data, offset=0, length=None):
        mv = memoryview(data)
        if offset < 0:
            raise ValueError("offset must be non-negative")
        if length is None:
            length = len(mv) - offset
        if length < 0:
            raise ValueError("length must be non-negative")
        end = offset + length
        if end > len(mv):
            raise ValueError("offset + length exceeds buffer size")
        self._base_view = mv
        self._offset = offset
        self._length = length
        self._view = mv[offset:end]

    @property
    def offset(self):
        return self._offset

    def __len__(self):
        return self._length

    def tobytes(self):
        '''Obtain bytes copy of this segment.'''
        return self._view.tobytes()
