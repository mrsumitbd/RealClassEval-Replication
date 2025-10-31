
class NoHashContext:
    '''No-op hash function.'''

    def __init__(self, data=None):
        '''Initialize'''
        self.data = bytearray()

        if data is not None:
            self.update(data)

    def update(self, data):
        '''Update data'''
        if isinstance(data, bytes):
            self.data.extend(data)
        else:
            raise TypeError("Data must be of type bytes")

    def digest(self):
        '''Final hash'''
        return bytes(self.data)

    def hexdigest(self):
        '''Hexadecimal digest.'''
        return self.digest().hex()
