
import struct
import contextlib
import io


class Reader:

    def __init__(self, stream):
        '''Create a non-capturing reader.'''
        self.stream = stream
        self.capture_stream = None

    def readfmt(self, fmt):
        '''Read a specified object, using a struct format string.'''
        size = struct.calcsize(fmt)
        data = self._read(size)
        return struct.unpack(fmt, data)

    def _read(self, size):
        if self.capture_stream is not None:
            data = self.stream.read(size)
            self.capture_stream.write(data)
            return data
        else:
            return self.stream.read(size)

    @contextlib.contextmanager
    def capture(self, stream):
        '''Temporarily capture the data read from the stream into the given stream.'''
        original_capture_stream = self.capture_stream
        self.capture_stream = stream
        try:
            yield
        finally:
            self.capture_stream = original_capture_stream


# Example usage:
if __name__ == "__main__":
    data = io.BytesIO(b'Hello, world!')
    reader = Reader(data)
    captured_data = io.BytesIO()
    with reader.capture(captured_data):
        print(reader.readfmt('4s'))  # prints: (b'Hell',)
    print(captured_data.getvalue())  # prints: b'Hell'
    print(reader.readfmt('8s'))  # prints: (b'o, world!',)
