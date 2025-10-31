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
        cls = self.__class__
        for name in dir(cls):
            try:
                if getattr(cls, name) is self:
                    return f"{cls.__module__}.{cls.__qualname__}.{name}"
            except Exception:
                continue
        return object.__repr__(self)

    @classmethod
    def iteritems(cls):
        '''
        Inspects attributes of the class for instances of the class
        and returns as key,value pairs mirroring dict#iteritems
        '''
        for name in dir(cls):
            if name.startswith('_'):
                continue
            try:
                val = getattr(cls, name)
            except Exception:
                continue
            if isinstance(val, cls):
                yield name, val
