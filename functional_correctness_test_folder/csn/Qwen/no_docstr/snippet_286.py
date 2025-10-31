
class AccessEnumMixin:

    @classmethod
    def validate(cls, level):
        return level in cls.__members__.values()

    def __str__(self):
        return self.name
