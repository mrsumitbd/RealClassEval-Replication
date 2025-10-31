
import contextlib
import struct


class Reader:

    def __init__(self, stream):
        '''Create a non-capturing reader.'''
        self.stream = stream
        self._capture_stream = None

    def readfmt(self, fmt):
        '''Read a specified object, using a struct format string.'''
        size = struct.calcsize(fmt)
        data = self.stream.read(size)
        if len(data) != size:
            raise EOFError("Unexpected end of stream")
        if self._capture_stream is not None:
            self._capture_stream.write(data)
        return struct.unpack(fmt, data)

    @contextlib.contextmanager
    def capture(self, stream):
        '''Context manager to capture read data into the given stream.'''
        prev_stream = self._capture_stream
        self._capture_stream = stream
        try:
            yield
        finally:
            self._capture_stream = prev_stream
