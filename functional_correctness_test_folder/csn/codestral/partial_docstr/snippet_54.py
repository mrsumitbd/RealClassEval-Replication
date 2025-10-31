
class Enum:

    def __init__(self, *args, **kwargs):
        self._value2member_map = {}
        for i, arg in enumerate(args):
            setattr(self, arg, i)
            self._value2member_map[i] = arg

    def __call__(self, val):
        '''Map an integer to the string representation.'''
        return self._value2member_map.get(val, None)
