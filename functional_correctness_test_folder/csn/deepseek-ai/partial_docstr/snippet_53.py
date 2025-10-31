
class Bits:

    def __init__(self, num_bits):
        self.num_bits = num_bits

    def __call__(self, val):
        return [bool((val >> i) & 1) for i in range(self.num_bits)]
