
class Enum:

    def __init__(self, *args, **kwargs):
        self._values = {name: value for name,
                        value in zip(args, range(len(args)))}
        self._values.update(kwargs)
        self._reverse = {value: name for name, value in self._values.items()}

    def __call__(self, val):
        if val in self._values:
            return self._values[val]
        elif val in self._reverse:
            return self._reverse[val]
        else:
            raise ValueError(f"Value {val} not found in Enum")
