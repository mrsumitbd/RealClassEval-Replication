class BufferSegment:
    def __init__(self, buffer=b"", offset=0, length=None):
        mv = memoryview(buffer)
        n = len(mv)
        if not isinstance(offset, int):
            raise TypeError("offset must be an int")
        if offset < 0 or offset > n:
            raise ValueError("offset out of range")
        if length is None:
            length = n - offset
        if not isinstance(length, int):
            raise TypeError("length must be an int or None")
        if length < 0 or offset + length > n:
            raise ValueError("length out of range")
        self._base = mv
        self._offset = offset
        self._view = mv[offset:offset + length]

    @property
    def offset(self):
        return self._offset

    def __len__(self):
        return len(self._view)

    def tobytes(self):
        return self._view.tobytes()
