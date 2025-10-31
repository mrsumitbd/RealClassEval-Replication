
class _MethodDocDescriptor:

    def __init__(self, session_weakref, class_name, name):
        '''Initialize the descriptor.'''
        self._session_weakref = session_weakref
        self._class_name = class_name
        self._name = name

    def __get__(self, instance, owner=None):
        '''Get the documentation.'''
        session = self._session_weakref()
        if session is None:
            return None
        cls = getattr(session, self._class_name, None)
        if cls is None:
            return None
        method = getattr(cls, self._name, None)
        if method is None:
            return None
        return method.__doc__
