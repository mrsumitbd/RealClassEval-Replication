class Enum:
    def __init__(self, *args, **kwargs):
        self._name_to_value = {}
        self._value_to_name = {}
        # Positional arguments are treated as names with auto‑incremented integer values
        for i, name in enumerate(args):
            if name in self._name_to_value:
                raise ValueError(f"Duplicate enum name: {name}")
            self._name_to_value[name] = i
            self._value_to_name[i] = name
        # Keyword arguments are treated as explicit name/value pairs
        for name, value in kwargs.items():
            if name in self._name_to_value:
                raise ValueError(f"Duplicate enum name: {name}")
            if value in self._value_to_name:
                raise ValueError(f"Duplicate enum value: {value}")
            self._name_to_value[name] = value
            self._value_to_name[value] = name

    def __call__(self, val):
        if isinstance(val, str):
            return self._name_to_value[val]
        return self._value_to_name[val]
