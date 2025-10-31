class OctavePtr:
    """A pointer to an Octave workspace value."""

    def __init__(self, session_weakref, name, address):
        """Initialize the pointer."""
        self._name = name
        self._address = address
        self._ref = session_weakref
        self.__module__ = 'oct2py.dynamic'
        self.__name__ = name

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address