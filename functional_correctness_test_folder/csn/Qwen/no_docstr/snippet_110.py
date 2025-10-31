
class Enum:

    def __repr__(self):
        return f"<{self.__class__.__name__}.{self.name}: {self.value}>"

    @classmethod
    def iteritems(cls):
        return ((name, value) for name, value in cls.__dict__.items() if not name.startswith('__'))
