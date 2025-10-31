class _PropertyAvailableIfDescriptor:
    """Implements a conditional property using the descriptor protocol based on the property decorator.

    The corresponding class in scikit-learn (`_AvailableIfDescriptor`) only supports callables.
    This class adopts the property decorator as described in the descriptor guide in the offical Python documentation.

    See also
    --------
    https://docs.python.org/3/howto/descriptor.html
        Descriptor HowTo Guide

    :class:`sklearn.utils.available_if._AvailableIfDescriptor`
        The original class in scikit-learn.
    """

    def __init__(self, check, fget, doc=None):
        self.check = check
        self.fget = fget
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc
        self._name = ''

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        attr_err = AttributeError(f'This {obj!r} has no attribute {self._name!r}')
        if not self.check(obj):
            raise attr_err
        if self.fget is None:
            raise AttributeError(f"property '{self._name}' has no getter")
        return self.fget(obj)