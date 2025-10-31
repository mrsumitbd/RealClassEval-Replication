
import weakref


class _MethodDocDescriptor:

    def __init__(self, session_weakref, class_name, name):
        self.session_weakref = weakref.ref(session_weakref)
        self.class_name = class_name
        self.name = name

    def __get__(self, instance, owner=None):
        session = self.session_weakref()
        if session is None:
            raise ReferenceError("Session has been garbage collected")
        return f"Documentation for {self.class_name}.{self.name} in session {id(session)}"
