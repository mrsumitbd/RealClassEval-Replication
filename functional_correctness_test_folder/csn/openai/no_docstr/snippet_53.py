class Bits:
    def __init__(self, num_bits):
        if not isinstance(num_bits, int) or num_bits <= 0:
            raise ValueError("num_bits must be a positive integer")
        self.num_bits = num_bits

    def __call__(self, val):
        if not isinstance(val, int):
            raise TypeError("val must be an integer")
        # Mask to the requested number of bits
        mask = (1 << self.num_bits) - 1
        val &= mask
        # Return bits as a tuple (MSB first)
        return tuple((val >> i) & 1 for i in reversed(range(self.num_bits)))
