
class AccessEnumMixin:
    '''Mixin for enum functionalities.'''
    @classmethod
    def validate(cls, level):
        '''Validate a string against the enum values.'''
        # If the level is already an enum member, return it
        if isinstance(level, cls):
            return level

        # Try to match the provided value with the enum members' values
        for member in cls:
            if member.value == level:
                return member

        # If no match is found, raise an error
        raise ValueError(f"{level!r} is not a valid {cls.__name__}")

    def __str__(self):
        '''Return its value.'''
        return str(self.value)
