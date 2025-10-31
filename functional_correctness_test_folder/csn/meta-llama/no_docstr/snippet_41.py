
class lazy_property:
    """
    A decorator that converts a method into a lazy property.
    The method is called only once when the property is first accessed.
    """

    def __init__(self, fget):
        self.fget = fget
        self.name = fget.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = self.fget(obj)
        setattr(obj, self.name, value)
        return value
