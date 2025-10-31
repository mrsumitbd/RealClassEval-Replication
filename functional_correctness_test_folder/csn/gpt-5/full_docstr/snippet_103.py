import contextlib
import struct


class Reader:
    '''Read basic type objects out of given stream.'''

    def __init__(self, stream):
        '''Create a non-capturing reader.'''
        self._stream = stream
        self._capture_stream = None

    def _read_exact(self, size):
        if size < 0:
            raise ValueError("size must be non-negative")
        chunks = []
        remaining = size
        while remaining:
            chunk = self._stream.read(remaining)
            if not chunk:
                raise EOFError(
                    f"unexpected end of stream; wanted {size} bytes, got {size - remaining}")
            chunks.append(chunk)
            remaining -= len(chunk)
        data = b"".join(chunks)
        if self._capture_stream is not None and data:
            self._capture_stream.write(data)
        return data

    def readfmt(self, fmt):
        '''Read a specified object, using a struct format string, or read `size` bytes if fmt is int.'''
        if isinstance(fmt, int):
            return self._read_exact(fmt)
        if isinstance(fmt, str):
            size = struct.calcsize(fmt)
            data = self._read_exact(size)
            values = struct.unpack(fmt, data)
            return values[0] if len(values) == 1 else values
        raise TypeError("fmt must be an int (size) or a struct format string")

    @contextlib.contextmanager
    def capture(self, stream):
        '''Capture all data read during this context.'''
        prev = self._capture_stream
        self._capture_stream = stream
        try:
            yield
        finally:
            self._capture_stream = prev
