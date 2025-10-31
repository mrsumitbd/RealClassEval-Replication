class Bits:
    '''Breaks an integer into a specified number of True/False bits.'''

    def __init__(self, num_bits):
        '''Initialize the number of bits.'''
        if not isinstance(num_bits, int) or num_bits < 0:
            raise ValueError("num_bits must be a non‑negative integer")
        self.num_bits = num_bits

    def __call__(self, val):
        '''Convert the integer to the list of True/False values.'''
        if not isinstance(val, int):
            raise TypeError("val must be an integer")
        # Mask to the requested number of bits (two's complement for negatives)
        mask = (1 << self.num_bits) - 1 if self.num_bits > 0 else 0
        val &= mask
        bits = []
        for i in range(self.num_bits - 1, -1, -1):
            bits.append(bool((val >> i) & 1))
        return bits
