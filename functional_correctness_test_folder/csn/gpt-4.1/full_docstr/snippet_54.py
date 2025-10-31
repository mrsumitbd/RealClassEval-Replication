
class Enum:
    '''Map values to specific strings.'''

    def __init__(self, *args, **kwargs):
        '''Initialize the mapping.'''
        self._map = {}
        # Positional arguments: list of strings, mapped to 0,1,2,...
        for idx, name in enumerate(args):
            self._map[idx] = name
        # Keyword arguments: int->str mapping
        for k, v in kwargs.items():
            self._map[k] = v

    def __call__(self, val):
        '''Map an integer to the string representation.'''
        return self._map[val]
