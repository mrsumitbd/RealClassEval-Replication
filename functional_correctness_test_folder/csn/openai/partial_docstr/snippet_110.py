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
        name = None
        for attr, val in vars(cls).items():
            if val is self:
                name = attr
                break
        if name is None:
            # Fallback to default representation
            return super().__repr__()
        # Build absolute dotted path: module.classname.attribute
        module = cls.__module__
        qualname = cls.__qualname__
        return f'{module}.{qualname}.{name}'

    @classmethod
    def iteritems(cls):
        '''
        Iterate over (name, value) pairs of class attributes
        that are instances of the Enum subclass.
        '''
        for name, value in vars(cls).items():
            if isinstance(value, cls):
                yield name, value
