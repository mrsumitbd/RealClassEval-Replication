from weakref import WeakKeyDictionary

class lazyval:
    """A memoizing property.

    Parameters
    ----------
    func : callable
        The function used to compute the value of the descriptor.
    """

    def __init__(self, func):
        self._cache = WeakKeyDictionary()
        self._func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        cache = self._cache
        try:
            return cache[instance]
        except KeyError:
            cache[instance] = val = self._func(instance)
            return val