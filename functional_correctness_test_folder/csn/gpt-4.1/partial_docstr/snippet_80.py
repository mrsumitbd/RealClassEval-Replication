
import warnings


class NiceRepr:
    '''
    Inherit from this class and define ``__nice__`` to "nicely" print your
    objects.
    Defines ``__str__`` and ``__repr__`` in terms of ``__nice__`` function
    Classes that inherit from :class:`NiceRepr` should redefine ``__nice__``.
    If the inheriting class has a ``__len__``, method then the default
    ``__nice__`` method will return its length.
    '''

    def __nice__(self):
        '''
        Returns:
            str
        '''
        # If __len__ is defined, use it as the default nice representation
        if hasattr(self, '__len__'):
            try:
                return str(len(self))
            except Exception:
                pass
        # Otherwise, fallback to default
        return 'object at {}'.format(hex(id(self)))

    def __repr__(self):
        '''
        Returns:
            str
        '''
        classname = self.__class__.__name__
        try:
            nice = self.__nice__()
        except Exception as ex:
            warnings.warn(
                'Error in __nice__ for {!r}: {}'.format(self.__class__, ex),
                RuntimeWarning,
                stacklevel=2
            )
            nice = '...'
        return '<{0}({1}) at {2}>'.format(classname, nice, hex(id(self)))

    def __str__(self):
        '''
        Returns:
            str
        '''
        classname = self.__class__.__name__
        try:
            nice = self.__nice__()
        except Exception as ex:
            warnings.warn(
                'Error in __nice__ for {!r}: {}'.format(self.__class__, ex),
                RuntimeWarning,
                stacklevel=2
            )
            nice = '...'
        return '<{0}({1})>'.format(classname, nice)
