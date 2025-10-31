
class AccessEnumMixin:
    '''Mixin for enum functionalities.'''
    @classmethod
    def validate(cls, level):
        '''Validate a string against the enum values.'''
        if level not in cls._value2member_map_:
            raise ValueError(f"{level} is not a valid {cls.__name__}")
        return cls._value2member_map_[level]

    def __str__(self):
        '''Return its value.'''
        return str(self.value)
