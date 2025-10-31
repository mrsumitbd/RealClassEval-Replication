import zlib

class YEnc:
    """A basic yEnc decoder.

    Keeps track of the CRC32 value as data is decoded.
    """

    def __init__(self) -> None:
        self.crc32 = 0
        self._escape = 0

    def decode(self, buf: bytes) -> bytes:
        data = bytearray()
        for b in buf:
            if self._escape:
                b = b - 106 & 255
                self._escape = 0
            elif b == 61:
                self._escape = 1
                continue
            elif b in {13, 10}:
                continue
            else:
                b = b - 42 & 255
            data.append(b)
        decoded = bytes(data)
        self.crc32 = zlib.crc32(decoded, self.crc32)
        return decoded