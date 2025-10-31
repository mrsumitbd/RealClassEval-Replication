
import struct
import contextlib


class Reader:

    def __init__(self, stream):
        '''Create a non-capturing reader.'''
        self._stream = stream
        self._capture_stack = []

    def readfmt(self, fmt):
        '''Read a specified object, using a struct format string.'''
        size = struct.calcsize(fmt)
        data = self._stream.read(size)
        if len(data) != size:
            raise EOFError("Not enough bytes to unpack")
        result = struct.unpack(fmt, data)
        if len(result) == 1:
            return result[0]
        return result

    @contextlib.contextmanager
    def capture(self, stream):
        '''Temporarily use a different stream for reading.'''
        self._capture_stack.append(self._stream)
        self._stream = stream
        try:
            yield
        finally:
            self._stream = self._capture_stack.pop()
