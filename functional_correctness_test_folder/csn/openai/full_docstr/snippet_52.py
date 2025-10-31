class BitField:
    '''Convert an integer to a string for each bit.'''

    def __init__(self, *names):
        '''Initialize the list of named bits.'''
        self.names = list(names)

    def __call__(self, val):
        '''Return a list with a string for each True bit in the integer.'''
        result = []
        for i, name in enumerate(self.names):
            if val & (1 << i):
                result.append(name)
        return result
