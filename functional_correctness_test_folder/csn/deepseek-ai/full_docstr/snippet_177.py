
import functools
from typing import Dict, Set, Callable, Any


class tracked_lru_cache:
    '''
    Decorator wrapping the functools.lru_cache adding a tracking of the
    functions that have been wrapped.
    Exposes a method to clear the cache of all the wrapped functions.
    Used to cache the parsed outputs in handlers/validators, to avoid
    multiple parsing of the same file.
    Allows Custodian to clear the cache after all the checks have been performed.
    '''

    _tracked_functions: Set[Callable] = set()

    def __init__(self, func: Callable) -> None:
        '''
        Args:
            func: function to be decorated.
        '''
        self.func = functools.lru_cache(func)
        tracked_lru_cache._tracked_functions.add(self.func)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        '''Call the decorated function.'''
        return self.func(*args, **kwargs)

    @classmethod
    def tracked_cache_clear(cls) -> None:
        '''Clear the cache of all the decorated functions.'''
        for func in cls._tracked_functions:
            func.cache_clear()
