
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
        class_obj = session.get_class(self._class_name)
        if class_obj is None:
            return None
        method_obj = getattr(class_obj, self._name, None)
        if method_obj is None:
            return None
        return method_obj.__doc__
