
class Enum:
    '''
    Object supporting CircuitPython-style of static symbols
    as seen with Direction.OUTPUT, Pull.UP
    '''

    def __init__(self, name):
        self._name = name

    def __repr__(self):
        for attr, value in vars(self.__class__).items():
            if value is self:
                return f"{self.__class__.__module__}.{self.__class__.__name__}.{attr}"
        return super().__repr__()

    @classmethod
    def iteritems(cls):
        for attr, value in vars(cls).items():
            if isinstance(value, cls):
                yield (attr, value)
