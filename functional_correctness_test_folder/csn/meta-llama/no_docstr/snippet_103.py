
import struct
import contextlib
import io


class Reader:

    def __init__(self, stream):
        self.stream = stream

    def readfmt(self, fmt):
        size = struct.calcsize(fmt)
        data = self.stream.read(size)
        if len(data) < size:
            raise EOFError('Not enough data to read')
        return struct.unpack(fmt, data)

    def read(self, size):
        data = self.stream.read(size)
        if len(data) < size:
            raise EOFError('Not enough data to read')
        return data

    @contextlib.contextmanager
    def capture(self, stream):
        original_stream = self.stream
        self.stream = stream
        try:
            yield self
        finally:
            self.stream = original_stream


# Example usage:
if __name__ == "__main__":
    data = b'Hello, World!'
    stream = io.BytesIO(data)
    reader = Reader(stream)
    print(reader.read(len(data)))  # prints: b'Hello, World!'

    stream = io.BytesIO(struct.pack('i', 12345))
    reader = Reader(stream)
    print(reader.readfmt('i'))  # prints: (12345,)

    stream = io.BytesIO(b'Hello')
    reader = Reader(stream)
    with reader.capture(io.BytesIO(b'Captured')) as captured_reader:
        print(captured_reader.read(8))  # prints: b'Captured'
    print(reader.read(5))  # prints: b'Hello'
