
class _MethodDocDescriptor:

    def __init__(self, session_weakref, class_name, name):
        self.session_weakref = session_weakref
        self.class_name = class_name
        self.name = name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        session = self.session_weakref()
        if session is None:
            raise RuntimeError("Session has been garbage collected")
        return session.get_method_documentation(self.class_name, self.name)
