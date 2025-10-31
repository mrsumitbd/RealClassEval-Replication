class _DocDescriptor:
    """An object that dynamically fetches the documentation
    for an Octave value.
    """

    def __init__(self, session_weakref, name):
        """Initialize the descriptor."""
        self.ref = session_weakref
        self.name = name
        self.doc = None

    def __get__(self, instance, owner=None):
        if self.doc:
            return self.doc
        self.doc = self.ref()._get_doc(self.name)
        return self.doc