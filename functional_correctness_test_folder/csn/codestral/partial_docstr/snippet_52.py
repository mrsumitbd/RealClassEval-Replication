
class BitField:
    '''Convert an integer to a string for each bit.'''

    def __init__(self, *names):
        '''Initialize the list of named bits.'''
        self.names = names

    def __call__(self, val):
        result = []
        for i, name in enumerate(self.names):
            if val & (1 << i):
                result.append(name)
        return ', '.join(result)
