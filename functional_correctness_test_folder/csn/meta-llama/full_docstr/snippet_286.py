
from enum import Enum


class AccessEnumMixin(Enum):
    '''Mixin for enum functionalities.'''

    @classmethod
    def validate(cls, level):
        '''Validate a string against the enum values.'''
        try:
            return cls[level]
        except KeyError:
            raise ValueError(f"'{level}' is not a valid {cls.__name__}")

    def __str__(self):
        '''Return its value.'''
        return self.value
