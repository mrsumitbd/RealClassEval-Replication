
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
        # Find the attribute name that refers to this instance
        for name, value in cls.__dict__.items():
            if value is self:
                return f'{cls.__module__}.{cls.__name__}.{name}'
        # Fallback if not found
        return f'<{cls.__module__}.{cls.__name__} instance>'

    @classmethod
    def iteritems(cls):
        '''
        Inspects attributes of the class for instances of the class
        and returns as key,value pairs mirroring dict#iteritems
        '''
        items = []
        for name, value in cls.__dict__.items():
            if isinstance(value, cls):
                items.append((name, value))
        return items
