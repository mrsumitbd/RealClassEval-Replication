
class lazy_property:
    '''Used to load numba first time it is needed.'''

    def __init__(self, fget):
        '''Lazy load a property with `fget`.'''
        self.fget = fget
        self.attr_name = None

    def __get__(self, obj, cls):
        '''Call the function, set the attribute.'''
        if obj is None:
            return self
        if self.attr_name is None:
            self.attr_name = f'_{self.fget.__name__}'
        if not hasattr(obj, self.attr_name):
            setattr(obj, self.attr_name, self.fget(obj))
        return getattr(obj, self.attr_name)
