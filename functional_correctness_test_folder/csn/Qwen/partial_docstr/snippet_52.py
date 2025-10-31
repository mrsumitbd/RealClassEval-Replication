
class BitField:
    '''Convert an integer to a string for each bit.'''

    def __init__(self, *names):
        '''Initialize the list of named bits.'''
        self.names = names

    def __call__(self, val):
        bit_strings = []
        for i, name in enumerate(reversed(self.names)):
            bit = (val >> i) & 1
            bit_strings.append(f"{name}: {bit}")
        return ", ".join(bit_strings)
