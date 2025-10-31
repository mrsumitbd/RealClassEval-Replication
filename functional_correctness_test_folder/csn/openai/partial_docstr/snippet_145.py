
import weakref


class _MethodDocDescriptor:
    """
    Descriptor that lazily retrieves method documentation from a session object.
    """

    def __init__(self, session_weakref, class_name, name):
        """
        Initialize the descriptor.

        Parameters
        ----------
        session_weakref : weakref.ref
            Weak reference to the session object that holds documentation.
        class_name : str
            Name of the class containing the method.
        name : str
            Name of the method whose documentation is requested.
        """
        # Store the weak reference to the session
        self._session_ref = session_weakref
        self._class_name = class_name
        self._method_name = name

    def __get__(self, instance, owner=None):
        """
        Retrieve the documentation for the method.

        Parameters
        ----------
        instance : object or None
            The instance on which the descriptor is accessed. If None,
            the descriptor is accessed through the class.
        owner : type or None
            The owner class.

        Returns
        -------
        str or None
            The documentation string for the method, or None if it cannot be
            retrieved.
        """
        # If accessed through the class, return the descriptor itself
        if instance is None:
            return self

        # Resolve the session from the weak reference
        session = self._session_ref() if callable(self._session_ref) else None
        if session is None:
            return None

        # Attempt to retrieve the documentation from the session
        try:
            # The session is expected to provide a method `get_method_doc`
            # that accepts a class name and method name.
            doc = session.get_method_doc(self._class_name, self._method_name)
            return doc
        except Exception:
            # If anything goes wrong (attribute missing, etc.), return None
            return None
