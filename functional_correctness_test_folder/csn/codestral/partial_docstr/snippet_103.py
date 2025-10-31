
import struct
import contextlib


class Reader:

    def __init__(self, stream):
        '''Create a non-capturing reader.'''
        self.stream = stream

    def readfmt(self, fmt):
        '''Read a specified object, using a struct format string.'''
        size = struct.calcsize(fmt)
        data = self.stream.read(size)
        return struct.unpack(fmt, data)

    @contextlib.contextmanager
    def capture(self, stream):
        '''Capture the stream and yield the reader.'''
        original_stream = self.stream
        self.stream = stream
        try:
            yield self
        finally:
            self.stream = original_stream
