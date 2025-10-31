
class AccessEnumMixin:
    '''Mixin for enum functionalities.'''
    @classmethod
    def validate(cls, level):
        '''Validate a string against the enum values.'''
        return level in cls.__members__.values()

    def __str__(self):
        '''Return its value.'''
        return self.value
