
class _MethodDocDescriptor:

    def __init__(self, session_weakref, class_name, name):
        self._session_weakref = session_weakref
        self._class_name = class_name
        self._name = name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        session = self._session_weakref()
        if session is None:
            return None
        return session.get_method_documentation(self._class_name, self._name)
