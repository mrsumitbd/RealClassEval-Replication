
class Enum:
    def __repr__(self):
        items = ', '.join(f"{k}={v!r}" for k, v in self.__class__.iteritems())
        return f"<Enum {self.__class__.__name__}: {items}>"

    @classmethod
    def iteritems(cls):
        for k, v in cls.__dict__.items():
            if not k.startswith('_') and not callable(v):
                yield (k, v)
