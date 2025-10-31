
import struct
import contextlib
import io


class Reader:
    '''Read basic type objects out of given stream.'''

    def __init__(self, stream):
        '''Create a non-capturing reader.'''
        self.stream = stream
        self.capture_stream = None

    def readfmt(self, fmt):
        '''Read a specified object, using a struct format string.'''
        size = struct.calcsize(fmt)
        data = self.read(size)
        return struct.unpack(fmt, data)

    def read(self, size):
        '''Read `size` bytes from stream.'''
        data = self.stream.read(size)
        if self.capture_stream is not None:
            self.capture_stream.write(data)
        return data

    @contextlib.contextmanager
    def capture(self, stream):
        '''Capture all data read during this context.'''
        self.capture_stream = stream
        try:
            yield
        finally:
            self.capture_stream = None


# Example usage:
if __name__ == "__main__":
    data = io.BytesIO(b'Hello, world!')
    reader = Reader(data)
    captured_data = io.BytesIO()
    with reader.capture(captured_data):
        print(reader.read(5))  # prints: b'Hello'
        print(reader.readfmt('5s'))  # prints: (b', wor',)
    print(captured_data.getvalue())  # prints: b'Hello, wor'
