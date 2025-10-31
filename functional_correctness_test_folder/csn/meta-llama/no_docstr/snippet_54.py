
class Enum:

    def __init__(self, *args, **kwargs):
        for i, arg in enumerate(args):
            setattr(self, arg, i)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __call__(self, val):
        for attr in dir(self):
            if not attr.startswith('__') and getattr(self, attr) == val:
                return attr
        raise ValueError(f"No enumeration value matches {val}")
