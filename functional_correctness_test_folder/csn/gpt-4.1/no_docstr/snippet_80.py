
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
        # Default: if __len__ is defined, return its value, else fallback
        if hasattr(self, '__len__') and callable(getattr(self, '__len__')):
            try:
                return str(len(self))
            except Exception:
                pass
        warnings.warn(
            'Class {} should override __nice__'.format(
                self.__class__.__name__),
            RuntimeWarning,
            stacklevel=2
        )
        return 'object at {}'.format(hex(id(self)))

    def __repr__(self):
        classname = self.__class__.__name__
        try:
            nice = self.__nice__()
        except Exception as ex:
            warnings.warn(
                '{}.__nice__() raised exception: {}'.format(classname, ex),
                RuntimeWarning,
                stacklevel=2
            )
            nice = '...'
        return '<{0}({1}) at {2}>'.format(classname, nice, hex(id(self)))

    def __str__(self):
        classname = self.__class__.__name__
        try:
            nice = self.__nice__()
        except Exception as ex:
            warnings.warn(
                '{}.__nice__() raised exception: {}'.format(classname, ex),
                RuntimeWarning,
                stacklevel=2
            )
            nice = '...'
        return '<{0}({1})>'.format(classname, nice)
