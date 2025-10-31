class NoHashContext:
    '''No-op hash function.'''

    def __init__(self, data=None):
        '''Initialize'''
        # No internal state needed for a no-op hash
        pass

    def update(self, data):
        '''Update data'''
        # No-op: ignore data
        pass

    def digest(self):
        '''Final hash'''
        # Return empty bytes as the hash value
        return b''

    def hexdigest(self):
        '''Hexadecimal digest.'''
        # Return empty string as the hex digest
        return ''
