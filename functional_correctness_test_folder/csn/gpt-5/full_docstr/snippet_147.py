class NoHashContext:
    '''No-op hash function.'''

    def __init__(self, data=None):
        '''Initialize'''
        self._data = bytearray()
        if data is not None:
            self.update(data)

    def update(self, data):
        '''Update data'''
        if data is None:
            return
        if isinstance(data, (bytes, bytearray, memoryview)):
            self._data.extend(bytes(data))
        elif isinstance(data, str):
            self._data.extend(data.encode('utf-8'))
        else:
            try:
                self._data.extend(memoryview(data).tobytes())
            except TypeError:
                raise TypeError("data must be bytes-like or str")

    def digest(self):
        '''Final hash'''
        return bytes(self._data)

    def hexdigest(self):
        '''Hexadecimal digest.'''
        return self._data.hex()
