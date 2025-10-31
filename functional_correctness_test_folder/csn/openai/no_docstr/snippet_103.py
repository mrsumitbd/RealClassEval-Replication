
import contextlib
import struct


class Reader:
    def __init__(self, stream):
        """
        Initialize the Reader with a binary stream.
        """
        self.stream = stream

    def readfmt(self, fmt):
        """
        Read data from the stream according to the given struct format string.
        Returns a tuple of unpacked values.
        """
        size = struct.calcsize(fmt)
        data = self.stream.read(size)
        if len(data) != size:
            raise EOFError(f"Expected {size} bytes, got {len(data)}")
        return struct.unpack(fmt, data)

    @contextlib.contextmanager
    def capture(self, stream):
        """
        Temporarily replace the Reader's stream with the given stream.
        Restores the original stream after the context exits.
        """
        original = self.stream
        self.stream = stream
        try:
            yield
        finally:
            self.stream = original
