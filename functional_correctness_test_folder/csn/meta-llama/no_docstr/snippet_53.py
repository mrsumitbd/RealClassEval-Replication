
class Bits:

    def __init__(self, num_bits):
        self.num_bits = num_bits
        self.mask = (1 << num_bits) - 1

    def __call__(self, val):
        return val & self.mask
