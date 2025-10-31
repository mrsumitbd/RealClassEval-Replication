
class BitField:

    def __init__(self, *names):
        self._names = names
        self._mask = 0

    def __call__(self, val):
        self._mask = val
        return self

    def __getattr__(self, name):
        if name in self._names:
            index = self._names.index(name)
            return bool(self._mask & (1 << index))
        raise AttributeError(f"'BitField' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name in ('_names', '_mask'):
            super().__setattr__(name, value)
        elif name in self._names:
            index = self._names.index(name)
            if value:
                self._mask |= (1 << index)
            else:
                self._mask &= ~(1 << index)
        else:
            raise AttributeError(
                f"'BitField' object has no attribute '{name}'")
