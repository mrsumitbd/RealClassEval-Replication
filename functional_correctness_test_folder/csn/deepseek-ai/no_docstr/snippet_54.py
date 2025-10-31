
class Enum:

    def __init__(self, *args, **kwargs):
        self._values = {}
        for i, arg in enumerate(args):
            self._values[arg] = i
        for key, val in kwargs.items():
            self._values[key] = val

    def __call__(self, val):
        for key, value in self._values.items():
            if value == val:
                return key
        raise ValueError(f"Value {val} not found in enum")
