
import struct
import contextlib


class Reader:
    '''Read basic type objects out of given stream.'''

    def __init__(self, stream):
        '''Create a non-capturing reader.'''
        self.stream = stream
        self.captured_data = None

    def readfmt(self, fmt):
        '''Read a specified object, using a struct format string.'''
        size = struct.calcsize(fmt)
        data = self.stream.read(size)
        if self.captured_data is not None:
            self.captured_data += data
        return struct.unpack(fmt, data)[0]

    def read(self, size):
        '''Read `size` bytes from stream.'''
        data = self.stream.read(size)
        if self.captured_data is not None:
            self.captured_data += data
        return data

    @contextlib.contextmanager
    def capture(self, stream):
        '''Capture all data read during this context.'''
        self.captured_data = b''
        try:
            yield self
        finally:
            stream.write(self.captured_data)
            self.captured_data = None
