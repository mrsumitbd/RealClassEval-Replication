
class _MethodDocDescriptor:
    '''An object that dynamically fetches the documentation
    for an Octave user class method.
        '''

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
        # Assume session has a method: get_method_doc(class_name, method_name)
        return session.get_method_doc(self._class_name, self._name)
