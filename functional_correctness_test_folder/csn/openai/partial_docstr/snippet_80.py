
import warnings


class NiceRepr:
    """
    Inherit from this class and define ``__nice__`` to "nicely" print your
    objects.
    Defines ``__str__`` and ``__repr__`` in terms of ``__nice__`` function.
    Classes that inherit from :class:`NiceRepr` should redefine ``__nice__``.
    If the inheriting class has a ``__len__`` method then the default
    ``__nice__`` method will return its length.
    """

    def __nice__(self):
        """
        Return a concise string representation of the object.
        Subclasses should override this method.  The default implementation
        returns the length of the object if it defines ``__len__``; otherwise
        it returns a warning string.
        """
        # Check if the subclass has overridden __nice__
        subclass_nice = type(self).__dict__.get('__nice__', None)
        if subclass_nice is not None and subclass_nice is not NiceRepr.__nice__:
            # The subclass has its own __nice__ implementation
            return subclass_nice(self)

        # Default behaviour
        if hasattr(self, '__len__'):
            try:
                return str(len(self))
            except Exception as e:
                warnings.warn(
                    f'NiceRepr: __len__ raised {e} for {type(self).__name__}',
                    RuntimeWarning,
                )
                return f'object at {hex(id(self))}'
        else:
            warnings.warn(
                f'NiceRepr: no __nice__ defined for {type(self).__name__}',
                RuntimeWarning,
            )
            return f'object at {hex(id(self))}'

    def __repr__(self):
        """
        Return a detailed representation of the object.
        """
        try:
            nice = self.__nice__()
        except Exception as e:
            warnings.warn(
                f'NiceRepr: __nice__ raised {e} for {type(self).__name__}',
                RuntimeWarning,
            )
            return f'<...{self.__class__.__name__} ...>'
        else:
            return (
                f'<{self.__class__.__name__}({nice}) at {hex(id(self))}>'
            )

    def __str__(self):
        """
        Return a concise representation of the object.
        """
        try:
            nice = self.__nice__()
        except Exception:
            return f'<...{self.__class__.__name__} ...>'
        else:
            return f'<{self.__class__.__name__}({nice})>'
