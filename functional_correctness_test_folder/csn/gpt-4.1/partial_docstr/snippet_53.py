
class Bits:

    def __init__(self, num_bits):
        '''Initialize the number of bits.'''
        self.num_bits = num_bits

    def __call__(self, val):
        '''Convert the integer to the list of True/False values.'''
        bits = []
        for i in range(self.num_bits - 1, -1, -1):
            bits.append(bool((val >> i) & 1))
        return bits
