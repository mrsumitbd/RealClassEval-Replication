
class BitField:

    def __init__(self, *names):
        self.names = names
        self.mask = 0
        self.shifts = {}
        for name in names:
            self.shifts[name] = self.mask.bit_length()
            self.mask |= 1 << self.shifts[name]

    def __call__(self, val):
        if not isinstance(val, int):
            raise ValueError("Value must be an integer")
        result = {}
        for name, shift in self.shifts.items():
            result[name] = (val >> shift) & 1
        return result
