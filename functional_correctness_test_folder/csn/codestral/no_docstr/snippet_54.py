
class Enum:

    def __init__(self, *args, **kwargs):
        self._value2member_map = {}
        for arg in args:
            if isinstance(arg, str):
                setattr(self, arg, arg)
                self._value2member_map[arg] = arg
            else:
                raise TypeError("Enum member names must be strings")

    def __call__(self, val):
        if val in self._value2member_map:
            return self._value2member_map[val]
        else:
            raise ValueError(f"{val} is not a valid {self.__class__.__name__}")
