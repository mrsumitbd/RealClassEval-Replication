
import struct
import contextlib


class Reader:

    def __init__(self, stream):
        self.stream = stream

    def readfmt(self, fmt):
        size = struct.calcsize(fmt)
        data = self.stream.read(size)
        if len(data) != size:
            raise EOFError("Not enough bytes to unpack")
        return struct.unpack(fmt, data)

    @contextlib.contextmanager
    def capture(self, stream):
        old_stream = self.stream
        self.stream = stream
        try:
            yield
        finally:
            self.stream = old_stream
