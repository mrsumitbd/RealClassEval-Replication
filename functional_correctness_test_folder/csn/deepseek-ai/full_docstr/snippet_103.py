
import contextlib
import struct


class Reader:
    '''Read basic type objects out of given stream.'''

    def __init__(self, stream):
        '''Create a non-capturing reader.'''
        self.stream = stream
        self.capture_stream = None

    def readfmt(self, fmt):
        '''Read a specified object, using a struct format string.'''
        size = struct.calcsize(fmt)
        data = self.stream.read(size)
        if len(data) != size:
            raise EOFError("Unexpected end of stream")
        if self.capture_stream is not None:
            self.capture_stream.write(data)
        return struct.unpack(fmt, data)

    def read(self, size):
        '''Read `size` bytes from stream.'''
        data = self.stream.read(size)
        if len(data) != size:
            raise EOFError("Unexpected end of stream")
        if self.capture_stream is not None:
            self.capture_stream.write(data)
        return data

    @contextlib.contextmanager
    def capture(self, stream):
        '''Capture all data read during this context.'''
        old_capture_stream = self.capture_stream
        self.capture_stream = stream
        try:
            yield
        finally:
            self.capture_stream = old_capture_stream
