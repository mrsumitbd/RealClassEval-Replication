class Bits:
    def __init__(self, num_bits):
        '''Initialize the number of bits.'''
        if not isinstance(num_bits, int) or num_bits <= 0:
            raise ValueError("num_bits must be a positive integer")
        self.num_bits = num_bits

    def __call__(self, val):
        '''Convert the integer to the list of True/False values.'''
        if not isinstance(val, int):
            raise TypeError("val must be an integer")
        # Mask to the specified number of bits
        mask = (1 << self.num_bits) - 1
        val &= mask
        bits = []
        for i in range(self.num_bits):
            bits.append(bool((val >> i) & 1))
        return bits
