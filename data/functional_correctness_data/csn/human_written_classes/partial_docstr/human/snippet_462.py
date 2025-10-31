import typing as ty

class ReadableStreamWrapper:
    """Bytes iterator wrapper that exposes a fileobj compatible `.read(n=None)`
    and `.close()` interface"""

    def __init__(self, generator: ty.Generator[bytes, ty.Any, ty.Any]):
        self._buffer = bytearray()
        self._generator = generator

    def read(self, length: ty.Optional[int]=None) -> bytes:
        if length is None:
            buffer = self._buffer
            for chunk in self._generator:
                buffer.extend(chunk)
            try:
                return bytes(buffer)
            finally:
                buffer.clear()
        if len(self._buffer) > 0:
            try:
                return bytes(self._buffer[0:length])
            finally:
                del self._buffer[0:length]
        try:
            chunk = b''
            while len(chunk) < 1:
                chunk = next(self._generator)
        except StopIteration:
            return b''
        else:
            try:
                return bytes(chunk[0:length])
            finally:
                self._buffer.extend(chunk[length:])

    def close(self) -> None:
        self._generator.close()
        self._buffer.clear()