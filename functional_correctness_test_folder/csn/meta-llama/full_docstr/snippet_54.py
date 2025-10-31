
class Enum:
    '''Map values to specific strings.'''

    def __init__(self, *args, **kwargs):
        '''Initialize the mapping.'''
        self.mapping = {}
        for i, arg in enumerate(args):
            self.mapping[i] = arg
        self.mapping.update(kwargs)

    def __call__(self, val):
        '''Map an integer to the string representation.'''
        return self.mapping.get(val, f"Unknown value: {val}")
