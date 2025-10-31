class BufferSegment:
    def __init__(self, buffer, offset=0, length=None):
        """
        Create a segment view into *buffer* starting at *offset* with the given *length*.
        If *length* is None, the segment extends to the end of the buffer.
        """
        self._buffer = memoryview(buffer)
        if offset < 0:
            raise ValueError("offset must be non‑negative")
        if length is None:
            length = len(self._buffer) - offset
        if length < 0:
            raise ValueError("length must be non‑negative")
        if offset + length > len(self._buffer):
            raise ValueError("segment exceeds buffer bounds")
        self._offset = offset
        self._length = length

    @property
    def offset(self):
        """Return the starting offset of the segment within the underlying buffer."""
        return self._offset

    def __len__(self):
        """Return the length of the segment."""
        return self._length

    def tobytes(self):
        """Return a bytes copy of the segment."""
        return self._buffer[self._offset: self._offset + self._length].tobytes()
