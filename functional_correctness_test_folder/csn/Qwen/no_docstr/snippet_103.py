
import struct
import contextlib
import io


class Reader:

    def __init__(self, stream):
        self.stream = stream

    def readfmt(self, fmt):
        size = struct.calcsize(fmt)
        data = self.stream.read(size)
        return struct.unpack(fmt, data)[0] if size == struct.calcsize('c') else struct.unpack(fmt, data)

    @contextlib.contextmanager
    def capture(self, stream):
        original_stream = self.stream
        self.stream = stream
        try:
            yield
        finally:
            self.stream = original_stream
