
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
        class_name = self.__class__.__name__
        for name, value in vars(self.__class__).items():
            if value is self:
                return f"{class_name}.{name}"
        return f"<{class_name} instance>"

    @classmethod
    def iteritems(cls):
        '''
        Yields (name, value) pairs for each enum member in the class.
        '''
        for name, value in vars(cls).items():
            if not name.startswith('_') and not callable(value):
                yield (name, value)
