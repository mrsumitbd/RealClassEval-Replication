class NoHashContext:
    def __init__(self, data=None):
        '''Initialize'''
        self._buffer = bytearray()
        if data is not None:
            self.update(data)

    def update(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes or bytearray")
        self._buffer.extend(data)

    def digest(self):
        '''Final hash'''
        return bytes(self._buffer)

    def hexdigest(self):
        '''Hexadecimal digest.'''
        return self._buffer.hex()
