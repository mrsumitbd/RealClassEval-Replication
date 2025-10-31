class StreamingFile:
    '''A file object wrapped around an iterator / data stream.'''

    def __init__(self, data_stream):
        '''Initialise the object with the data stream.'''
        self._iter = iter(data_stream)
        self._buffer = bytearray()
        self._exhausted = False

    def read(self, size=None):
        '''Read bytes from an iterator.'''
        if size is None or (isinstance(size, int) and size < 0):
            if not self._exhausted:
                for chunk in self._iter:
                    self._buffer.extend(bytes(chunk))
                self._exhausted = True
            data = bytes(self._buffer)
            self._buffer.clear()
            return data

        if not isinstance(size, int):
            raise TypeError("size must be an integer or None")

        if size == 0:
            return b""

        # Ensure buffer has at least 'size' bytes or iterator is exhausted
        while len(self._buffer) < size and not self._exhausted:
            try:
                chunk = next(self._iter)
            except StopIteration:
                self._exhausted = True
                break
            self._buffer.extend(bytes(chunk))

        # Serve from buffer
        if size >= len(self._buffer):
            data = bytes(self._buffer)
            self._buffer.clear()
            return data
        else:
            data = bytes(self._buffer[:size])
            del self._buffer[:size]
            return data
