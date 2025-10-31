
class BitField:
    '''Convert an integer to a string for each bit.'''

    def __init__(self, *names):
        '''Initialize the list of named bits.'''
        self.names = names

    def __call__(self, val):
        '''Return a string representation of the bits.'''
        bits = []
        for i, name in enumerate(self.names):
            if val & (1 << i):
                bits.append(name)
        return ' '.join(bits)
