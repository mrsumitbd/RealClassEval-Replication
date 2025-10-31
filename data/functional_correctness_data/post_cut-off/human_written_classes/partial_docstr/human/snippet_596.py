class Crc32Stream:
    """CRC32 stream processing class for incremental calculation."""

    def __init__(self):
        self._poly = 3988292384
        self._crc = 0
        self._bytes = [0] * 256
        self.reset()

    def reset(self) -> None:
        """Reset the state of the CRC32 stream."""
        self._crc = 0 ^ 4294967295
        for n in range(256):
            c = n
            for _ in range(8):
                if c & 1:
                    c = self._poly ^ c >> 1
                else:
                    c = c >> 1
            self._bytes[n] = c & 4294967295

    def append(self, data: bytes | str) -> str:
        """
        Append new data to the CRC32 stream and update the checksum.

        Args:
            data: The data to append (bytes or string)

        Returns:
            The updated CRC32 checksum as a hexadecimal string
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        crc = self._crc
        for byte in data:
            crc = crc >> 8 ^ self._bytes[(crc ^ byte) & 255]
        self._crc = crc
        return number_to_hex(crc ^ 4294967295)

    @property
    def crc32(self) -> str:
        """Get the current CRC32 checksum."""
        return number_to_hex(self._crc ^ 4294967295)