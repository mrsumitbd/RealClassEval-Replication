
class BitField:

    def __init__(self, *names):
        self.names = names
        self.mask = {name: 1 << i for i, name in enumerate(names)}

    def __call__(self, val):
        return {name: bool(val & mask) for name, mask in self.mask.items()}
