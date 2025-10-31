class lazy_property:

    def __init__(self, fget):
        self.fget = fget
        self.attr_name = fget.__name__
        self.__doc__ = getattr(fget, "__doc__", None)

    def __get__(self, obj, cls):
        if obj is None:
            return self
        if self.attr_name in obj.__dict__:
            return obj.__dict__[self.attr_name]
        value = self.fget(obj)
        obj.__dict__[self.attr_name] = value
        return value
