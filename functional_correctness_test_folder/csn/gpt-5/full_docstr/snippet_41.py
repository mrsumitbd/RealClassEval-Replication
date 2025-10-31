class lazy_property:
    '''Used to load numba first time it is needed.'''

    def __init__(self, fget):
        '''Lazy load a property with `fget`.'''
        self.fget = fget
        self.name = fget.__name__
        self.__doc__ = getattr(fget, '__doc__')

    def __get__(self, obj, cls):
        '''Call the function, set the attribute.'''
        if obj is None:
            return self
        if self.name in obj.__dict__:
            return obj.__dict__[self.name]
        value = self.fget(obj)
        setattr(obj, self.name, value)
        return value
