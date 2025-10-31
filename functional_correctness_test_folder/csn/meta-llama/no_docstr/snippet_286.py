
from enum import Enum


class AccessEnumMixin:

    @classmethod
    def validate(cls, level):
        if not isinstance(level, cls):
            raise TypeError(
                f"Expected {cls.__name__}, got {type(level).__name__}")
        return level

    def __str__(self):
        return self.name

# Example usage:


class AccessLevel(AccessEnumMixin, Enum):
    READ = 1
    WRITE = 2
    DELETE = 3


# Test the implementation
if __name__ == "__main__":
    try:
        AccessLevel.validate("READ")
    except TypeError as e:
        print(e)

    level = AccessLevel.validate(AccessLevel.READ)
    print(level)  # Output: READ
    print(str(level))  # Output: READ
