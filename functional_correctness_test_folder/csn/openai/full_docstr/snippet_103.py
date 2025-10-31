
import io
import struct
import contextlib


class Reader:
    '''Read basic type objects out of given stream.'''

    def __init__(self, stream):
        '''Create a non‑capturing reader.'''
        self.stream = stream

    def readfmt(self, fmt):
        '''Read a specified object, using a struct format string.'''
        size = struct.calcsize(fmt)
        data = self.stream.read(size)
        if len(data) != size:
            raise EOFError(
                "Unexpected end of stream while reading format '{}'".format(fmt))
        return struct.unpack(fmt, data)

    def read(self, size):
        '''Read `size` bytes from stream.'''
        data = self.stream.read(size)
        if len(data) != size:
            raise EOFError(
                "Unexpected end of stream while reading {} bytes".format(size))
        return data

    @contextlib.contextmanager
    def capture(self, stream):
        '''Capture all data read during this context.'''
        original_read = stream.read
        captured = io.BytesIO()

        def read_wrapper(n=-1):
            data = original_read(n)
            captured.write(data)
            return data

        stream.read = read_wrapper
        try:
            yield captured
        finally:
            stream.read = original_read
