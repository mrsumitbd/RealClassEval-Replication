
from enum import Enum


class AccessEnumMixin:
    @classmethod
    def validate(cls, level):
        if not isinstance(level, cls):
            try:
                level = cls(level)
            except ValueError:
                raise ValueError(f"Invalid {cls.__name__} level: {level}")
        return level

    def __str__(self):
        return self.value


# Example usage:
class AccessLevel(AccessEnumMixin, Enum):
    READ = 'read'
    WRITE = 'write'
    DELETE = 'delete'


# Testing the class
if __name__ == "__main__":
    print(AccessLevel.validate('read'))  # AccessLevel.READ
    print(AccessLevel.validate(AccessLevel.WRITE))  # AccessLevel.WRITE
    try:
        print(AccessLevel.validate('invalid'))
    except ValueError as e:
        print(e)  # Invalid AccessLevel level: invalid
    print(str(AccessLevel.DELETE))  # delete
