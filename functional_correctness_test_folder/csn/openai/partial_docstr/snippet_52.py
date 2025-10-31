class BitField:
    '''Convert an integer to a string for each bit.'''

    def __init__(self, *names):
        '''Initialize the list of named bits.'''
        self.names = list(names)

    def __call__(self, val):
        '''Return a string representation of the bits of `val` using the stored names.'''
        parts = []
        for i, name in enumerate(self.names):
            bit = (val >> i) & 1
            parts.append(f'{name}={bit}')
        return ' '.join(parts)
