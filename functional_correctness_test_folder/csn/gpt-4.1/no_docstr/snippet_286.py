
class AccessEnumMixin:
    _levels = {'guest', 'user', 'admin', 'superuser'}

    @classmethod
    def validate(cls, level):
        if level not in cls._levels:
            raise ValueError(f"Invalid access level: {level}")
        return level

    def __str__(self):
        return self.__class__.__name__
