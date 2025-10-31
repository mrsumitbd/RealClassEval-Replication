
class Enum:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        items = [f"{key}={value}" for key,
                 value in self.__dict__.items() if not key.startswith('__')]
        return f"{self.__class__.__name__}({', '.join(items)})"

    @classmethod
    def iteritems(cls):
        for key, value in cls.__dict__.items():
            if not key.startswith('__') and not callable(value):
                yield key, value


# Example usage:
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


print(Color.RED)  # Output: Color(RED=1)
for key, value in Color.iteritems():
    print(f"{key}: {value}")
