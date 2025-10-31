import contextlib
import struct


class Reader:

    def __init__(self, stream):
        self.stream = stream

    def _read_exact(self, n):
        if n < 0:
            raise ValueError("size must be non-negative")
        data = bytearray()
        read = getattr(self.stream, "read", None)
        if read is None:
            raise TypeError("stream must have a read() method")
        while len(data) < n:
            chunk = read(n - len(data))
            if chunk is None:
                raise IOError("stream.read() returned None")
            if chunk == b"" or chunk == "":
                raise EOFError("unexpected end of stream")
            if isinstance(chunk, str):
                # Fallback if the stream is text-mode; best-effort 1:1 mapping
                chunk = chunk.encode("latin-1")
            data.extend(chunk)
        return bytes(data)

    def _readfmt_impl(self, fmt):
        s = struct.Struct(fmt)
        data = self._read_exact(s.size)
        out = s.unpack(data)
        return out[0] if len(out) == 1 else out

    def readfmt(self, fmt):
        return self._readfmt_impl(fmt)

    def readfmt(self, fmt):
        return self._readfmt_impl(fmt)

    @contextlib.contextmanager
    def capture(self, stream):
        old = self.stream
        self.stream = stream
        try:
            yield self
        finally:
            self.stream = old
