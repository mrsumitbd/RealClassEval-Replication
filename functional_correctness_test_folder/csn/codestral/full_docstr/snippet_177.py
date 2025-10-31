
import functools


class tracked_lru_cache:
    '''
    Decorator wrapping the functools.lru_cache adding a tracking of the
    functions that have been wrapped.
    Exposes a method to clear the cache of all the wrapped functions.
    Used to cache the parsed outputs in handlers/validators, to avoid
    multiple parsing of the same file.
    Allows Custodian to clear the cache after all the checks have been performed.
    '''

    _wrapped_functions = []

    def __init__(self, func) -> None:
        '''
        Args:
            func: function to be decorated.
        '''
        self._func = func
        self._cache = functools.lru_cache(maxsize=None)(func)
        tracked_lru_cache._wrapped_functions.append(self._cache)

    def __call__(self, *args, **kwargs):
        '''Call the decorated function.'''
        return self._cache(*args, **kwargs)

    @classmethod
    def tracked_cache_clear(cls) -> None:
        '''Clear the cache of all the decorated functions.'''
        for func in cls._wrapped_functions:
            func.cache_clear()
