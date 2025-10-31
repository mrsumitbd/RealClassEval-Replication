
class Enum:
    '''
    Object supporting CircuitPython-style of static symbols
    as seen with Direction.OUTPUT, Pull.UP
    '''

    def __repr__(self):
        '''
        Assumes instance will be found as attribute of own class.
        Returns dot-subscripted path to instance
        (assuming absolute import of containing package)
        '''
        for cls in type(self).__mro__:
            for name, value in vars(cls).items():
                if value is self:
                    return f'{cls.__module__}.{cls.__qualname__}.{name}'
        return super().__repr__()

    @classmethod
    def iteritems(cls):
        '''
        Inspects attributes of the class for instances of the class
        and returns as key,value pairs mirroring dict#iteritems
        '''
        return ((name, value) for name, value in vars(cls).items() if isinstance(value, cls))
