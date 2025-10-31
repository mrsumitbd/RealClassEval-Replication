
class AccessEnumMixin:
    '''Mixin for enum functionalities.'''
    @classmethod
    def validate(cls, level):
        '''Validate a string against the enum values.'''
        return any(level == item.value for item in cls)

    def __str__(self):
        '''Return its value.'''
        return str(self.value)
