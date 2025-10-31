
class NoHashContext:
    '''No-op hash function.'''

    def __init__(self, data=None):
        '''Initialize'''
        pass

    def update(self, data):
        '''Update data'''
        pass

    def digest(self):
        '''Final hash'''
        return b''

    def hexdigest(self):
        '''Hexadecimal digest.'''
        return ''
