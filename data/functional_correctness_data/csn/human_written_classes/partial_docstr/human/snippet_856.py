class MarkerObject:
    """Replaces None in cases when None value is also expected.
    Used mainly by caches to describe a cache miss.

    """

    def __init__(self, name):
        if isinstance(name, bytes):
            raise TypeError('name must be str, not bytes')
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name