class Memoize:

    def __init__(self, function):
        self._cache = {}
        self._callable = function

    def __call__(self, *args, **kwds):
        cache = self._cache
        key = self._getKey(*args, **kwds)
        try:
            return cache[key]
        except KeyError:
            cachedValue = cache[key] = self._callable(*args, **kwds)
            return cachedValue

    def _getKey(self, *args, **kwds):
        return kwds and (args, ImmutableDict(kwds)) or args