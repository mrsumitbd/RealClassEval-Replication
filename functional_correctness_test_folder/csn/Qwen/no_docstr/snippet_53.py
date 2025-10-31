
class Bits:

    def __init__(self, num_bits):
        self.num_bits = num_bits

    def __call__(self, val):
        return format(val, f'0{self.num_bits}b')
