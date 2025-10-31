
class BufferSegment:
    """
    Represents a contiguous segment of a buffer (bytes, bytearray, or memoryview).
    """

    def __init__(self, buffer, offset=0, length=None):
        """
        Parameters
        ----------
        buffer : bytes | bytearray | memoryview
            The underlying buffer.
        offset : int, optional
            The starting index of the segment within the buffer.
        length : int | None, optional
            The length of the segment. If None, the segment extends to the end of the buffer.
        """
        if not isinstance(buffer, (bytes, bytearray, memoryview)):
            raise TypeError("buffer must be bytes, bytearray, or memoryview")

        self._buffer = memoryview(buffer)
        if not isinstance(offset, int):
            raise TypeError("offset must be an integer")
        if offset < 0 or offset > len(self._buffer):
            raise ValueError("offset out of range")

        if length is None:
            length = len(self._buffer) - offset
        if not isinstance(length, int):
            raise TypeError("length must be an integer or None")
        if length < 0 or offset + length > len(self._buffer):
            raise ValueError("length out of range")

        self._offset = offset
        self._length = length

    @property
    def offset(self):
        """The starting index of the segment within the underlying buffer."""
        return self._offset

    def __len__(self):
        """The length of the segment."""
        return self._length

    def tobytes(self):
        """Return the segment as an immutable bytes object."""
        return self._buffer[self._offset: self._offset + self._length].tobytes()
