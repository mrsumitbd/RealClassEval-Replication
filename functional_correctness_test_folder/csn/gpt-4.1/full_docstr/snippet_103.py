
import struct
import contextlib


class Reader:
    '''Read basic type objects out of given stream.'''

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
        if self._capture_stack:
            self._capture_stack[-1].append(data)
        result = struct.unpack(fmt, data)
        if len(result) == 1:
            return result[0]
        return result

    def read(self, size):
        '''Read `size` bytes from stream.'''
        data = self._stream.read(size)
        if len(data) != size:
            raise EOFError("Not enough bytes to read")
        if self._capture_stack:
            self._capture_stack[-1].append(data)
        return data

    @contextlib.contextmanager
    def capture(self, stream):
        '''Capture all data read during this context.'''
        self._capture_stack.append([])
        try:
            yield
            captured = b''.join(self._capture_stack.pop())
            stream.write(captured)
        finally:
            if self._capture_stack and len(self._capture_stack[-1]) == 0:
                self._capture_stack.pop()
