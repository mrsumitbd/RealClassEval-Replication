
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
        for name, value in self.__class__.__dict__.items():
            if value is self:
                return f"{self.__class__.__name__}.{name}"
        raise ValueError("Instance not found as attribute of its class")

    @classmethod
    def iteritems(cls):
        for name, value in cls.__dict__.items():
            if isinstance(value, cls):
                yield name, value
