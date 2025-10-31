
class BitField:

    def __init__(self, *names):
        self.names = names
        self.mask = {name: 1 << i for i, name in enumerate(names)}
        self.reverse_mask = {v: k for k, v in self.mask.items()}

    def __call__(self, val):
        class BitFieldValue:
            def __init__(self, val, mask, reverse_mask):
                self.val = val
                self.mask = mask
                self.reverse_mask = reverse_mask

            def __getattr__(self, name):
                if name in self.mask:
                    return (self.val & self.mask[name]) != 0
                else:
                    raise AttributeError(
                        f"'BitFieldValue' object has no attribute '{name}'")

            def __setattr__(self, name, value):
                if name in ['val', 'mask', 'reverse_mask']:
                    super().__setattr__(name, value)
                elif name in self.mask:
                    if value:
                        self.val |= self.mask[name]
                    else:
                        self.val &= ~self.mask[name]
                else:
                    raise AttributeError(
                        f"'BitFieldValue' object has no attribute '{name}'")

            def __int__(self):
                return self.val

            def __repr__(self):
                set_bits = [self.reverse_mask[mask]
                            for mask in self.reverse_mask if self.val & mask]
                return f"BitFieldValue({self.val:#x}, {', '.join(set_bits)})"

        return BitFieldValue(val, self.mask, self.reverse_mask)
