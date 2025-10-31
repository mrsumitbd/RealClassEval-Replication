class Bits:
    '''Breaks an integer into a specified number of True/False bits.'''

    def __init__(self, num_bits):
        '''Initialize the number of bits.'''
        if not isinstance(num_bits, int):
            raise TypeError("num_bits must be an integer")
        if num_bits <= 0:
            raise ValueError("num_bits must be a positive integer")
        self.num_bits = num_bits

    def __call__(self, val):
        '''Convert the integer to the list of True/False values.'''
        if not isinstance(val, int):
            raise TypeError("val must be an integer")
        if val < 0:
            raise ValueError("val must be non-negative")
        max_val = (1 << self.num_bits) - 1
        if val > max_val:
            raise ValueError(
                f"val {val} cannot be represented in {self.num_bits} bits")
        return [bool((val >> i) & 1) for i in range(self.num_bits - 1, -1, -1)]
