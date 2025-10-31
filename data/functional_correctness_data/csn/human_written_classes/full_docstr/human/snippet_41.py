import functools

class lazy_property:
    """Used to load numba first time it is needed."""

    def __init__(self, fget):
        """Lazy load a property with `fget`."""
        self.fget = fget
        functools.update_wrapper(self, fget)

    def __get__(self, obj, cls):
        """Call the function, set the attribute."""
        if obj is None:
            return self
        value = self.fget(obj)
        setattr(obj, self.fget.__name__, value)
        return value