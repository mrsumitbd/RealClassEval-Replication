
class NoHashContext:

    def __init__(self, data=None):
        '''Initialize'''
        self._data = bytearray()
        if data is not None:
            self.update(data)

    def update(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        self._data.extend(data)

    def digest(self):
        '''Final hash'''
        return bytes(self._data)

    def hexdigest(self):
        '''Hexadecimal digest.'''
        return self.digest().hex()
