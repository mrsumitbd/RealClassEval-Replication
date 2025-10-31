
class lazy_property:
    '''Used to load numba first time it is needed.'''

    def __init__(self, fget):
        '''Lazy load a property with `fget`.'''
        self.fget = fget
        self.name = fget.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return self
        # Compute the value only once and cache it on the instance
        value = self.fget(obj)
        setattr(obj, self.name, value)
        return value
