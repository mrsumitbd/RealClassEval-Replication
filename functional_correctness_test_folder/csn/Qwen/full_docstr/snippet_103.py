
import struct
import contextlib


class Reader:
    '''Read basic type objects out of given stream.'''

    def __init__(self, stream):
        '''Create a non-capturing reader.'''
        self.stream = stream
        self.captured_data = bytearray()

    def readfmt(self, fmt):
        '''Read a specified object, using a struct format string.'''
        size = struct.calcsize(fmt)
        data = self.stream.read(size)
        return struct.unpack(fmt, data)[0]

    def read(self, size):
        '''Read `size` bytes from stream.'''
        data = self.stream.read(size)
        if self.captured_data:
            self.captured_data.extend(data)
        return data

    @contextlib.contextmanager
    def capture(self):
        '''Capture all data read during this context.'''
        original_captured_data = self.captured_data
        self.captured_data = bytearray()
        try:
            yield
        finally:
            captured = bytes(self.captured_data)
            self.captured_data = original_captured_data
            return captured
