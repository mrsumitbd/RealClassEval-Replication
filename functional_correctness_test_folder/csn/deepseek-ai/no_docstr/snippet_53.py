
class Bits:

    def __init__(self, num_bits):
        self.num_bits = num_bits

    def __call__(self, val):
        max_val = (1 << self.num_bits) - 1
        return val & max_val
