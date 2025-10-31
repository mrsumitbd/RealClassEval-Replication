
class _MethodDocDescriptor:

    def __init__(self, session_weakref, class_name, name):
        self.session_weakref = session_weakref
        self.class_name = class_name
        self.name = name

    def __get__(self, instance, owner=None):
        from weakref import ref
        session = self.session_weakref()
        if session is None:
            return None
        doc = session.get_method_doc(self.class_name, self.name)
        return doc
