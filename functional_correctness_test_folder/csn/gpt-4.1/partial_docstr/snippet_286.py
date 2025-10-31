
class AccessEnumMixin:

    @classmethod
    def validate(cls, level):
        if not hasattr(cls, '__members__'):
            raise AttributeError(
                f"{cls.__name__} must define __members__ dict")
        if level not in cls.__members__:
            raise ValueError(f"{level} is not a valid {cls.__name__}")
        return cls.__members__[level]

    def __str__(self):
        return str(self.value)
