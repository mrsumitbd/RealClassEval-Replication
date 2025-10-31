
class Bits:

    def __init__(self, num_bits):

        self.num_bits = num_bits

    def __call__(self, val):

        return val & ((1 << self.num_bits) - 1)
