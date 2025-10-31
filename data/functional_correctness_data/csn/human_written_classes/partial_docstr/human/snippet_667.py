from binascii import crc32, hexlify

class CRC32Context:
    """Hash context that uses CRC32."""
    __slots__ = ['_crc']

    def __init__(self, data=None):
        self._crc = 0
        if data:
            self.update(data)

    def update(self, data):
        """Process data."""
        self._crc = crc32(data, self._crc)

    def digest(self):
        """Final hash."""
        return self._crc

    def hexdigest(self):
        """Hexadecimal digest."""
        return '%08x' % self.digest()