
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
    _tracked_functions = set()

    def __init__(self, maxsize=128, typed=False):
        self.maxsize = maxsize
        self.typed = typed

    def __call__(self, func):
        wrapped_func = functools.lru_cache(
            maxsize=self.maxsize, typed=self.typed)(func)
        tracked_lru_cache._tracked_functions.add(wrapped_func)
        return wrapped_func

    @classmethod
    def tracked_cache_clear(cls) -> None:
        for func in cls._tracked_functions:
            func.cache_clear()
