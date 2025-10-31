
class Enum:

    def __init__(self, *args, **kwargs):
        self._members = {}
        self._reverse = {}
        idx = 0
        for name in args:
            self._members[name] = idx
            self._reverse[idx] = name
            idx += 1
        for name, value in kwargs.items():
            self._members[name] = value
            self._reverse[value] = name

    def __call__(self, val):
        if isinstance(val, str):
            return self._members[val]
        else:
            return self._reverse[val]
