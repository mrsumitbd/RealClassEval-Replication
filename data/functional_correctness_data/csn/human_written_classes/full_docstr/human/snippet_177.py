import functools
from typing import ClassVar

class tracked_lru_cache:
    """
    Decorator wrapping the functools.lru_cache adding a tracking of the
    functions that have been wrapped.

    Exposes a method to clear the cache of all the wrapped functions.

    Used to cache the parsed outputs in handlers/validators, to avoid
    multiple parsing of the same file.
    Allows Custodian to clear the cache after all the checks have been performed.
    """
    cached_functions: ClassVar = set()

    def __init__(self, func) -> None:
        """
        Args:
            func: function to be decorated.
        """
        self.func = functools.lru_cache(func)
        functools.update_wrapper(self, func)
        self.cache_info = self.func.cache_info
        self.cache_clear = self.func.cache_clear

    def __call__(self, *args, **kwargs):
        """Call the decorated function."""
        result = self.func(*args, **kwargs)
        self.cached_functions.add(self.func)
        return result

    @classmethod
    def tracked_cache_clear(cls) -> None:
        """Clear the cache of all the decorated functions."""
        while cls.cached_functions:
            f = cls.cached_functions.pop()
            f.cache_clear()