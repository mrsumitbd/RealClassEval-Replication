
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
            for name in dir(cls):
                if getattr(cls, name) is self:
                    return f'{cls.__module__}.{cls.__qualname__}.{name}'
        return repr(self)

    @classmethod
    def iteritems(cls):
        for name in dir(cls):
            val = getattr(cls, name)
            if isinstance(val, cls):
                yield (name, val)
