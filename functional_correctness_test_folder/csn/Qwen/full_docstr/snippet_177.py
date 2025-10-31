
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

    _tracked_functions = []

    def __init__(self, func) -> None:
        '''
        Args:
            func: function to be decorated.
        '''
        self.func = func
        self.cache = functools.lru_cache()(func)
        tracked_lru_cache._tracked_functions.append(self)

    def __call__(self, *args, **kwargs):
        '''Call the decorated function.'''
        return self.cache(*args, **kwargs)

    @classmethod
    def tracked_cache_clear(cls) -> None:
        '''Clear the cache of all the decorated functions.'''
        for func_wrapper in cls._tracked_functions:
            func_wrapper.cache.cache_clear()
