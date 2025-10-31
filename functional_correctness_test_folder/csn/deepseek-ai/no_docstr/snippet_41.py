
class lazy_property:

    def __init__(self, fget):
        self.fget = fget
        self.attr_name = fget.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = self.fget(obj)
        setattr(obj, self.attr_name, value)
        return value
