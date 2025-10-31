
import contextlib
import struct


class Reader:
    def __init__(self, stream):
        '''Create a non-capturing reader.'''
        self.stream = stream

    def readfmt(self, fmt):
        '''Read a specified object, using a struct format string.'''
        size = struct.calcsize(fmt)
        data = self.stream.read(size)
        if len(data) < size:
            raise EOFError("Not enough data to unpack")
        result = struct.unpack(fmt, data)
        return result[0] if len(result) == 1 else result

    @contextlib.contextmanager
    def capture(self, stream):
        '''Temporarily replace the reader's stream with another stream.'''
        old_stream = self.stream
        self.stream = stream
        try:
            yield
        finally:
            self.stream = old_stream
