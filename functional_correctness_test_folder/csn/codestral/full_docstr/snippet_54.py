
class Enum:
    '''Map values to specific strings.'''

    def __init__(self, *args, **kwargs):
        '''Initialize the mapping.'''
        self._map = {}
        for arg in args:
            if isinstance(arg, tuple) and len(arg) == 2:
                self._map[arg[0]] = arg[1]
        for key, value in kwargs.items():
            self._map[key] = value

    def __call__(self, val):
        '''Map an integer to the string representation.'''
        return self._map.get(val, None)
