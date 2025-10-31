class lazy_property:
    '''Used to load numba first time it is needed.'''

    def __init__(self, fget):
        '''Lazy load a property with `fget`.'''
        self.fget = fget
        self.name = fget.__name__

    def __get__(self, obj, cls):
        '''Call the function, set the attribute.'''
        if obj is None:
            return self
        # Compute the value once
        value = self.fget(obj)
        # Cache the value on the instance
        setattr(obj, self.name, value)
        return value
