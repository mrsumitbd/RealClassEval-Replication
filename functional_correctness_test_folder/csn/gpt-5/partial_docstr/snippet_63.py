class StreamingFile:
    '''A file object wrapped around an iterator / data stream.'''

    def __init__(self, data_stream):
        '''Initialise the object with the data stream.'''
        self._iter = iter(data_stream)
        self._buffer = None
        self._eof = False

    def _empty_like(self):
        if self._buffer is not None:
            return self._buffer[:0]
        return ''

    def read(self, size=None):
        if size is None or (isinstance(size, int) and size < 0):
            if self._eof:
                return self._empty_like()
            chunks = []
            if self._buffer is not None:
                chunks.append(self._buffer)
            try:
                for chunk in self._iter:
                    chunks.append(chunk)
            finally:
                self._eof = True
            if not chunks:
                # unknown type and empty
                return ''
            first = chunks[0]
            if isinstance(first, (bytes, bytearray)):
                out = b''.join(chunks)
                self._buffer = first[:0]
                return out
            else:
                out = ''.join(chunks)
                self._buffer = first[:0]
                return out

        if size == 0:
            return self._empty_like()

        if self._eof and (self._buffer is None or len(self._buffer) == 0):
            return self._empty_like()

        # Ensure buffer has at least 'size' bytes/chars, or stream exhausted
        current_len = 0 if self._buffer is None else len(self._buffer)
        while (size is None or current_len < size) and not self._eof:
            try:
                chunk = next(self._iter)
                if self._buffer is None:
                    self._buffer = chunk
                else:
                    self._buffer += chunk
                current_len = len(self._buffer)
            except StopIteration:
                self._eof = True
                break

        if self._buffer is None or len(self._buffer) == 0:
            return self._empty_like()

        # Slice out the requested amount
        if size is None:
            result = self._buffer
            self._buffer = self._buffer[:0]
            return result

        result = self._buffer[:size]
        self._buffer = self._buffer[size:]
        return result
