
class BufferSegment:
    '''Represents a segment within a ``BufferWithSegments``.
    This type is essentially a reference to N bytes within a
    ``BufferWithSegments``.
    The object conforms to the buffer protocol.
    '''

    def __init__(self, buffer, offset, length):
        """
        Parameters
        ----------
        buffer : bytes-like
            The underlying buffer that this segment refers to.
        offset : int
            The starting byte offset of the segment within *buffer*.
        length : int
            The length of the segment in bytes.
        """
        # Store a memoryview of the underlying buffer to avoid copying
        self._buffer = memoryview(buffer)
        self._offset = int(offset)
        self._length = int(length)

        if self._offset < 0 or self._length < 0:
            raise ValueError("offset and length must be non‑negative")
        if self._offset + self._length > len(self._buffer):
            raise ValueError("segment extends beyond the underlying buffer")

    @property
    def offset(self):
        '''The byte offset of this segment within its parent buffer.'''
        return self._offset

    def __len__(self):
        '''Obtain the length of the segment, in bytes.'''
        return self._length

    def tobytes(self):
        '''Obtain bytes copy of this segment.'''
        return self._buffer[self._offset:self._offset + self._length].tobytes()

    # Optional: expose the buffer protocol so that ``memoryview`` can be used
    def __buffer__(self, flags, offset=0, length=None):
        """Return a memoryview of the segment."""
        # The buffer protocol expects a memoryview object
        seg = self._buffer[self._offset:self._offset + self._length]
        return seg

    def __repr__(self):
        return (f"{self.__class__.__name__}(offset={self._offset}, "
                f"length={self._length})")
