class Enum:

    def __repr__(self):
        cls = type(self)
        items = ", ".join(f"{k}={v!r}" for k, v in cls.iteritems())
        return f"<{cls.__name__} {items}>"

    @classmethod
    def iteritems(cls):
        for k, v in cls.__dict__.items():
            if k.startswith('_'):
                continue
            if isinstance(v, (staticmethod, classmethod)):
                continue
            if callable(v):
                continue
            yield k, v
