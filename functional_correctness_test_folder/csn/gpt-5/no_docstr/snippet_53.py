class Bits:

    def __init__(self, num_bits):
        if not isinstance(num_bits, int):
            raise TypeError("num_bits must be an integer")
        if num_bits <= 0:
            raise ValueError("num_bits must be a positive integer")
        self.num_bits = num_bits
        self.mask = (1 << num_bits) - 1

    def __call__(self, val):
        if not isinstance(val, int):
            raise TypeError("val must be an integer")
        return val & self.mask
