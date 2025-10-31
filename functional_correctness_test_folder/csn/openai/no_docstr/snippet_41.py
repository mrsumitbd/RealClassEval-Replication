class lazy_property:
    def __init__(self, fget):
        self.fget = fget
        self.attr_name = fget.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return self
        if self.attr_name not in obj.__dict__:
            obj.__dict__[self.attr_name] = self.fget(obj)
        return obj.__dict__[self.attr_name]
