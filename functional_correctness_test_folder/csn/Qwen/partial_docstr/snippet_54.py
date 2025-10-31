
class Enum:

    def __init__(self, *args, **kwargs):
        self._values = {}
        self._names = {}
        for i, name in enumerate(args):
            self._values[i] = name
            self._names[name] = i
        self._values.update(kwargs)
        for name, value in kwargs.items():
            self._names[value] = name

    def __call__(self, val):
        '''Map an integer to the string representation.'''
        return self._values.get(val, None)
