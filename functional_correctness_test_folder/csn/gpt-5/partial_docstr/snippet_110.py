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
        # Search for a class (subclass of Enum) that has this instance bound as an attribute
        def all_subclasses(cls):
            seen = set()
            stack = [cls]
            while stack:
                c = stack.pop()
                for sc in c.__subclasses__():
                    if sc not in seen:
                        seen.add(sc)
                        stack.append(sc)
                        yield sc

        # Prefer subclasses; also consider the base Enum in case attributes are placed directly on it
        candidate_classes = list(all_subclasses(Enum)) + [Enum]

        for owner in candidate_classes:
            for name, value in vars(owner).items():
                if value is self:
                    return f"{owner.__module__}.{owner.__name__}.{name}"
        return object.__repr__(self)

    @classmethod
    def iteritems(cls):
        for name, value in vars(cls).items():
            if not name.startswith('_') and isinstance(value, Enum):
                yield name, value
