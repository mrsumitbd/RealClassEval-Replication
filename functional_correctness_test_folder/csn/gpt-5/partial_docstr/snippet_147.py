class NoHashContext:

    def __init__(self, data=None):
        '''Initialize'''
        self._buffer = bytearray()
        if data is not None:
            self.update(data)

    def update(self, data):
        if data is None:
            raise TypeError("a bytes-like object is required, not NoneType")
        if isinstance(data, str):
            data = data.encode()
        self._buffer.extend(memoryview(data).tobytes())

    def digest(self):
        '''Final hash'''
        return bytes(self._buffer)

    def hexdigest(self):
        '''Hexadecimal digest.'''
        return self.digest().hex()
