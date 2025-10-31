import struct
import contextlib


class Reader:

    def __init__(self, stream):
        '''Create a non-capturing reader.'''
        self.stream = stream
        self._capture_stack = []

    def readfmt(self, fmt):
        '''Read a specified object, using a struct format string.'''
        return self._readfmt(fmt)

    def _readfmt(self, fmt):
        size = struct.calcsize(fmt)
        data = self.stream.read(size)
        if data is None or len(data) != size:
            raise EOFError(
                "Unexpected end of stream while reading formatted data")
        for cap in self._capture_stack:
            cap.write(data)
        values = struct.unpack(fmt, data)
        return values[0] if len(values) == 1 else values

    def readfmt(self, fmt):
        return self._readfmt(fmt)

    @contextlib.contextmanager
    def capture(self, stream):
        self._capture_stack.append(stream)
        try:
            yield
        finally:
            self._capture_stack.pop()
