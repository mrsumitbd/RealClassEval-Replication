
class AccessEnumMixin:

    @classmethod
    def validate(cls, level):
        if level not in cls._value2member_map_:
            raise ValueError(f"{level} is not a valid {cls.__name__}")
        return cls._value2member_map_[level]

    def __str__(self):
        return str(self.value)
