
class Enum:

    def __repr__(self):
        return f"<{self.__class__.__name__}.{self.name}>"

    @classmethod
    def iteritems(cls):
        for name, value in vars(cls).items():
            if not name.startswith('_') and not callable(value):
                yield name, value
