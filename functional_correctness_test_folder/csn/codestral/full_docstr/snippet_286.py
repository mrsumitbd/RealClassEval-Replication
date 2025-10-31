
class AccessEnumMixin:
    '''Mixin for enum functionalities.'''
    @classmethod
    def validate(cls, level):
        '''Validate a string against the enum values.'''
        if not isinstance(level, str):
            raise ValueError("Level must be a string")
        if level not in cls._value2member_map_:
            raise ValueError(f"Invalid level: {level}")
        return True

    def __str__(self):
        '''Return its value.'''
        return self.value
