
class Enum:

    def __init__(self, *args, **kwargs):
        self.enum_dict = {}
        for arg in args:
            if isinstance(arg, tuple) and len(arg) == 2:
                self.enum_dict[arg[0]] = arg[1]
            else:
                self.enum_dict[arg] = arg
        self.enum_dict.update(kwargs)
        self.reverse_enum_dict = {v: k for k, v in self.enum_dict.items()}

    def __call__(self, val):
        '''Map an integer to the string representation.'''
        if isinstance(val, int):
            return self.enum_dict.get(val, None)
        elif isinstance(val, str):
            return self.reverse_enum_dict.get(val, None)
        else:
            raise TypeError("Input must be either int or str")
