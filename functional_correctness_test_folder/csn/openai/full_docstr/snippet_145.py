
import weakref


class _MethodDocDescriptor:
    '''An object that dynamically fetches the documentation
    for an Octave user class method.
    '''

    def __init__(self, session_weakref, class_name, name):
        '''Initialize the descriptor.'''
        # Store a weak reference to the Octave session to avoid reference cycles
        self._session_ref = weakref.ref(session_weakref)
        self._class_name = class_name
        self._method_name = name
        self._doc = None  # Cache the documentation once fetched

    def __get__(self, instance, owner=None):
        '''Get the documentation.'''
        # If the descriptor is accessed via the class, instance will be None.
        # We always return the documentation string.
        if self._doc is None:
            session = self._session_ref()
            if session is None:
                # Session has been garbage‑collected; cannot fetch docstring
                self._doc = ''
            else:
                # Attempt to fetch the documentation from the Octave session.
                # The exact API may vary; we try a few common patterns.
                try:
                    # Preferred: use a dedicated method if available
                    self._doc = session.get_method_doc(
                        self._class_name, self._method_name)
                except AttributeError:
                    try:
                        # Fallback: use the generic help command
                        full_name = f'{self._class_name}::{self._method_name}'
                        self._doc = session.help(full_name)
                    except Exception:
                        # If all attempts fail, return an empty string
                        self._doc = ''
        return self._doc
