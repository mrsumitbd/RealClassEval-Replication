
class lazy_property:
    '''Used to load numba first time it is needed.'''

    def __init__(self, fget):
        '''Lazy load a property with `fget`.'''
        self.fget = fget
        self.attr_name = fget.__name__

    def __get__(self, obj, cls):
        '''Call the function, set the attribute.'''
        if obj is None:
            return self
        value = self.fget(obj)
        setattr(obj, self.attr_name, value)
        return value
