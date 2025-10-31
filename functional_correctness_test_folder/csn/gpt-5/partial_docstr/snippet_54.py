class Enum:

    def __init__(self, *args, **kwargs):
        self._name_to_value = {}
        self._value_to_name = {}
        if args and kwargs:
            raise TypeError(
                "Provide either positional names or keyword mappings, not both.")
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            args = tuple(args[0])
        if kwargs:
            items = list(kwargs.items())
        else:
            items = [(name, idx) for idx, name in enumerate(args)]
        for name, value in items:
            if not isinstance(name, str):
                raise TypeError("Enum name must be a string.")
            if not isinstance(value, int):
                raise TypeError("Enum value must be an int.")
            if name in self._name_to_value:
                raise ValueError(f"Duplicate enum name: {name}")
            if value in self._value_to_name:
                raise ValueError(f"Duplicate enum value: {value}")
            self._name_to_value[name] = value
            self._value_to_name[value] = name
            setattr(self, name, value)

    def __call__(self, val):
        '''Map an integer to the string representation.'''
        if not isinstance(val, int):
            raise TypeError("Enum value must be an int.")
        try:
            return self._value_to_name[val]
        except KeyError:
            raise ValueError(f"{val} is not a valid enum value.")
