
class AccessEnumMixin:

    @classmethod
    def validate(cls, level):
        if level not in cls.__members__.values():
            raise ValueError(
                f"Invalid level: {level}. Must be one of {list(cls.__members__.values())}")

    def __str__(self):
        '''Return its value.'''
        return str(self.value)
