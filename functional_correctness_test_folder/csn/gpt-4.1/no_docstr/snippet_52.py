
class BitField:

    def __init__(self, *names):
        self.names = names
        self.name_to_bit = {name: 1 << i for i, name in enumerate(names)}
        self.bit_to_name = {1 << i: name for i, name in enumerate(names)}

    def __call__(self, val):
        result = []
        for i, name in enumerate(self.names):
            if val & (1 << i):
                result.append(name)
        return result
