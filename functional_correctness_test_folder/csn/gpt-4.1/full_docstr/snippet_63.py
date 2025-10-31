
class StreamingFile:
    '''A file object wrapped around an iterator / data stream.'''

    def __init__(self, data_stream):
        '''Initialise the object with the data stream.'''
        self._stream = iter(data_stream)
        self._buffer = b''

    def read(self, size=None):
        '''Read bytes from an iterator.'''
        if size is None:
            # Read all remaining data
            chunks = [self._buffer]
            self._buffer = b''
            for chunk in self._stream:
                chunks.append(chunk)
            return b''.join(chunks)
        else:
            # Read up to size bytes
            result = bytearray()
            # Use buffer first
            if self._buffer:
                take = min(size, len(self._buffer))
                result += self._buffer[:take]
                self._buffer = self._buffer[take:]
                size -= take
                if size == 0:
                    return bytes(result)
            # Read from stream
            try:
                while size > 0:
                    chunk = next(self._stream)
                    if len(chunk) <= size:
                        result += chunk
                        size -= len(chunk)
                    else:
                        result += chunk[:size]
                        self._buffer = chunk[size:]
                        size = 0
            except StopIteration:
                pass
            return bytes(result)
