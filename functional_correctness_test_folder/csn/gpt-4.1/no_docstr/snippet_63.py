
class StreamingFile:

    def __init__(self, data_stream):
        self._stream = data_stream
        self._buffer = b""
        self._exhausted = False

    def read(self, size=None):
        if size is None:
            # Read all remaining data
            chunks = [self._buffer]
            self._buffer = b""
            for chunk in self._stream:
                chunks.append(chunk)
            self._exhausted = True
            return b"".join(chunks)
        else:
            # Read up to 'size' bytes
            result = bytearray()
            # Use buffer first
            if self._buffer:
                take = min(size, len(self._buffer))
                result += self._buffer[:take]
                self._buffer = self._buffer[take:]
                size -= take
            # Read from stream if needed
            while size > 0 and not self._exhausted:
                try:
                    chunk = next(self._stream)
                except StopIteration:
                    self._exhausted = True
                    break
                if len(chunk) <= size:
                    result += chunk
                    size -= len(chunk)
                else:
                    result += chunk[:size]
                    self._buffer = chunk[size:] + self._buffer
                    size = 0
            return bytes(result)
