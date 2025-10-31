
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

    def __getitem__(self, key):
        # Support slicing and indexing
        if isinstance(key, slice):
            start, stop, step = key.indices(self._length)
            new_offset = self._offset + start
            new_length = stop - start
            if step != 1:
                # Return a bytes object for non-unit step
                return bytes(self._parent_buffer[self._offset:self._offset + self._length])[key]
            return BufferSegment(self._parent_buffer, new_offset, new_length)
        elif isinstance(key, int):
            if key < 0:
                key += self._length
            if key < 0 or key >= self._length:
                raise IndexError("index out of range")
            return self._parent_buffer[self._offset + key]
        else:
            raise TypeError("Invalid argument type")

    def __bytes__(self):
        return self.tobytes()

    def __repr__(self):
        return f"<BufferSegment offset={self._offset} length={self._length}>"

    def __eq__(self, other):
        if isinstance(other, BufferSegment):
            return self.tobytes() == other.tobytes()
        elif isinstance(other, (bytes, bytearray, memoryview)):
            return self.tobytes() == bytes(other)
        return NotImplemented

    def __memoryview__(self):
        return memoryview(self._parent_buffer)[self._offset:self._offset + self._length]

    def __getbuffer__(self, *args, **kwargs):
        # For buffer protocol (CPython uses __buffer__ or __getbuffer__)
        return memoryview(self._parent_buffer)[self._offset:self._offset + self._length]
