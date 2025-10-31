
class lazy_property:
    '''Used to load numba first time it is needed.'''

    def __init__(self, fget):
        '''Lazy load a property with `fget`.'''
        self.fget = fget
        self.attr_name = f"_lazy_{fget.__name__}"

    def __get__(self, obj, cls):
        if obj is None:
            return self
        if not hasattr(obj, self.attr_name):
            value = self.fget(obj)
            setattr(obj, self.attr_name, value)
            return value
        return getattr(obj, self.attr_name)
