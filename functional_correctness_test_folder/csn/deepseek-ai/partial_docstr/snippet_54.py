
class Enum:

    def __init__(self, *args, **kwargs):
        self._value_to_name = {}
        self._name_to_value = {}

        for i, name in enumerate(args):
            self._value_to_name[i] = name
            self._name_to_value[name] = i

        for name, value in kwargs.items():
            self._value_to_name[value] = name
            self._name_to_value[name] = value

    def __call__(self, val):
        '''Map an integer to the string representation.'''
        return self._value_to_name.get(val)
