
import weakref


class _MethodDocDescriptor:
    """
    Descriptor that lazily retrieves the documentation string of a method
    defined on a class associated with a session object.

    Parameters
    ----------
    session_weakref : weakref.ref
        Weak reference to the session instance that owns the descriptor.
    class_name : str
        Name of the class that contains the method.
    name : str
        Name of the method whose documentation is to be retrieved.
    """

    def __init__(self, session_weakref, class_name, name):
        # Store the weak reference and identifiers
        self._session_ref = session_weakref
        self._class_name = class_name
        self._method_name = name

    def __get__(self, instance, owner=None):
        """
        Retrieve the method's docstring when accessed through an instance.

        If accessed through the class (instance is None), return the descriptor
        itself so that it can be introspected.
        """
        if instance is None:
            # Accessed on the class, return the descriptor itself
            return self

        # Resolve the session from the weak reference
        session = self._session_ref()
        if session is None:
            raise ReferenceError(
                "Session reference has been garbage collected")

        # Attempt to locate the target class on the session
        # The session is expected to expose the class via an attribute
        # named exactly as `self._class_name`. If not found, raise an error.
        cls = getattr(session, self._class_name, None)
        if cls is None:
            raise AttributeError(
                f"Session object has no attribute '{self._class_name}'"
            )

        # Retrieve the method from the class
        method = getattr(cls, self._method_name, None)
        if method is None:
            raise AttributeError(
                f"Class '{self._class_name}' has no method '{self._method_name}'"
            )

        # Return the method's docstring
        return method.__doc__
