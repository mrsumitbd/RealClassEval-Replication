class _MethodDocDescriptor:
    """An object that dynamically fetches the documentation
    for an Octave user class method.
    """

    def __init__(self, session_weakref, class_name, name):
        """Initialize the descriptor."""
        self.ref = session_weakref
        self.class_name = class_name
        self.name = name
        self.doc = None

    def __get__(self, instance, owner=None):
        """Get the documentation."""
        if self.doc is not None:
            return self.doc
        session = self.ref()
        class_name = self.class_name
        method = self.name
        doc = session._get_doc(f'@{class_name}/{method}')
        self.doc = doc or session._get_doc(method)
        return self.doc