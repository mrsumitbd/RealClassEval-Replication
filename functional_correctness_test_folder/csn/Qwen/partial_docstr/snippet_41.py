
class lazy_property:
    '''Used to load numba first time it is needed.'''

    def __init__(self, fget):
        '''Lazy load a property with `fget`.'''
        self.fget = fget
        self.func_name = fget.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = self.fget(obj)
        setattr(obj, self.func_name, value)
        return value
