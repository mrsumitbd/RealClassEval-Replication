
class AccessEnumMixin:

    @classmethod
    def validate(cls, level):

        if not isinstance(level, cls):
            raise ValueError(
                f"Invalid level: {level}. Must be an instance of {cls.__name__}")
        return level

    def __str__(self):

        return self.name
