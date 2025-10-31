
class StreamingFile:
    '''A file object wrapped around an iterator / data stream.'''

    def __init__(self, data_stream):
        '''Initialise the object with the data stream.'''
        self._stream = iter(data_stream)
        self._buffer = ''
        self._eof = False

    def read(self, size=None):
        if self._eof:
            return ''
        if size is None:
            # Read all remaining data
            chunks = [self._buffer]
            self._buffer = ''
            for chunk in self._stream:
                chunks.append(chunk)
            self._eof = True
            return ''.join(chunks)
        else:
            # Read up to size characters
            result = []
            remaining = size
            # Use buffer first
            if self._buffer:
                if len(self._buffer) >= remaining:
                    result.append(self._buffer[:remaining])
                    self._buffer = self._buffer[remaining:]
                    return ''.join(result)
                else:
                    result.append(self._buffer)
                    remaining -= len(self._buffer)
                    self._buffer = ''
            # Read from stream
            while remaining > 0:
                try:
                    chunk = next(self._stream)
                except StopIteration:
                    self._eof = True
                    break
                if len(chunk) > remaining:
                    result.append(chunk[:remaining])
                    self._buffer = chunk[remaining:]
                    remaining = 0
                else:
                    result.append(chunk)
                    remaining -= len(chunk)
            return ''.join(result)
