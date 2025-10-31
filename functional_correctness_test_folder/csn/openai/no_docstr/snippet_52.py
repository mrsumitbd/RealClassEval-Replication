class BitField:
    def __init__(self, *names):
        self.names = list(names)

    def __call__(self, val):
        return {name: bool((val >> i) & 1) for i, name in enumerate(self.names)}
