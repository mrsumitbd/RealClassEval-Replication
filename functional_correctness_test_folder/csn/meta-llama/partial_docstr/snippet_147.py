
class NoHashContext:

    def __init__(self, data=None):
        '''Initialize'''
        self.data = bytearray()
        if data is not None:
            self.update(data)

    def update(self, data):
        '''Update the hash object with the bytes-like object.'''
        if isinstance(data, bytearray):
            self.data.extend(data)
        elif isinstance(data, bytes):
            self.data.extend(data)
        else:
            raise TypeError("Data must be bytes or bytearray")

    def digest(self):
        '''Final hash (returns the original data).'''
        return bytes(self.data)

    def hexdigest(self):
        '''Hexadecimal digest (returns the hexadecimal representation of the original data).'''
        return self.digest().hex()
