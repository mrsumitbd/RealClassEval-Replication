
class NoHashContext:

    def __init__(self, data=None):
        '''Initialize'''
        self.data = data if data is not None else b''

    def update(self, data):
        self.data += data

    def digest(self):
        '''Final hash'''
        return self.data

    def hexdigest(self):
        '''Hexadecimal digest.'''
        return self.data.hex()
