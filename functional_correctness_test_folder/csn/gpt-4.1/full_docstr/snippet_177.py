
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

    _tracked_wrapped_funcs = []

    def __init__(self, func) -> None:
        '''
        Args:
            func: function to be decorated.
        '''
        self._original_func = func
        self._wrapped_func = functools.lru_cache()(func)
        tracked_lru_cache._tracked_wrapped_funcs.append(self._wrapped_func)

    def __call__(self, *args, **kwargs):
        '''Call the decorated function.'''
        return self._wrapped_func(*args, **kwargs)

    @classmethod
    def tracked_cache_clear(cls) -> None:
        '''Clear the cache of all the decorated functions.'''
        for wrapped_func in cls._tracked_wrapped_funcs:
            wrapped_func.cache_clear()
