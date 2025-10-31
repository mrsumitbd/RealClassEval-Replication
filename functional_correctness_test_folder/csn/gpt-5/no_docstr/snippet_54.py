class Enum:

    def __init__(self, *args, **kwargs):
        self._names = {}
        values = []
        if len(args) == 1 and hasattr(args[0], '__iter__') and not isinstance(args[0], (str, bytes)):
            values = list(args[0])
        else:
            values = list(args)
        for name, val in kwargs.items():
            self._names[name] = val
        self._values = set(values) | set(self._names.values())

    def __call__(self, val):
        if val in self._names:
            return self._names[val]
        if val in self._values:
            return val
        raise ValueError(
            f"Invalid enum value: {val}. Allowed: {sorted(self._values)} or names: {sorted(self._names.keys())}")
