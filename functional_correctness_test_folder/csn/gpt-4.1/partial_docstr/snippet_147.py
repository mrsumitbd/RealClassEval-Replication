
class NoHashContext:

    def __init__(self, data=None):
        '''Initialize'''
        self._data = b''
        if data is not None:
            self.update(data)

    def update(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        self._data += data

    def digest(self):
        '''Final hash'''
        return self._data

    def hexdigest(self):
        '''Hexadecimal digest.'''
        return self._data.hex()
