
class Bits:

    def __init__(self, num_bits):
        self.num_bits = num_bits

    def __call__(self, val):
        if not isinstance(val, int):
            raise TypeError("Value must be an integer")
        mask = (1 << self.num_bits) - 1
        return val & mask
