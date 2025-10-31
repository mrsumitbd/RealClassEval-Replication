
import weakref


class _MethodDocDescriptor:
    '''An object that dynamically fetches the documentation
    for an Octave user class method.
        '''

    def __init__(self, session_weakref, class_name, name):
        '''Initialize the descriptor.'''
        self.session_weakref = weakref.ref(session_weakref)
        self.class_name = class_name
        self.name = name

    def __get__(self, instance, owner=None):
        '''Get the documentation.'''
        session = self.session_weakref()
        if session is None:
            raise ReferenceError("Session has been garbage collected")
        return session.get_method_doc(self.class_name, self.name)
