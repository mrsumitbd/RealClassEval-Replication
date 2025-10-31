class StreamingFile:
    '''A file object wrapped around an iterator / data stream.'''

    def __init__(self, data_stream):
        '''Initialise the object with the data stream.'''
        self._stream = iter(data_stream)
        self._buffer = b''

    def read(self, size=None):
        '''Read up to size bytes from the stream. If size is None or negative, read all remaining data.'''
        # Handle reading all data
        if size is None or size < 0:
            chunks = [self._buffer]
            self._buffer = b''
            for chunk in self._stream:
                if isinstance(chunk, str):
                    chunk = chunk.encode()
                chunks.append(chunk)
            return b''.join(chunks)

        # Handle zero or negative size explicitly
        if size == 0:
            return b''

        # Ensure we have enough data in the buffer
        while len(self._buffer) < size:
            try:
                chunk = next(self._stream)
            except StopIteration:
                break
            if isinstance(chunk, str):
                chunk = chunk.encode()
            self._buffer += chunk

        # Slice the required amount
        result = self._buffer[:size]
        self._buffer = self._buffer[size:]
        return result
