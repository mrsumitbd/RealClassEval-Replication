
import struct
import contextlib


class Reader:

    def __init__(self, stream):
        '''Create a non-capturing reader.'''
        self.stream = stream
        self.capturing = False
        self.captured_data = bytearray()

    def readfmt(self, fmt):
        '''Read a specified object, using a struct format string.'''
        size = struct.calcsize(fmt)
        data = self.stream.read(size)
        if self.capturing:
            self.captured_data.extend(data)
        return struct.unpack(fmt, data)[0]

    @contextlib.contextmanager
    def capture(self, stream):
        original_stream = self.stream
        self.stream = stream
        self.capturing = True
        self.captured_data = bytearray()
        try:
            yield
        finally:
            self.stream = original_stream
            self.capturing = False
            captured_bytes = bytes(self.captured_data)
            self.captured_data = bytearray()
            yield captured_bytes
