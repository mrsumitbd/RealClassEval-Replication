
import functools
from typing import Callable, Any, Tuple, Dict


class tracked_lru_cache:
    """
    Decorator wrapping the functools.lru_cache adding a tracking of the
    functions that have been wrapped.
    Exposes a method to clear the cache of all the wrapped functions.
    Used to cache the parsed outputs in handlers/validators, to avoid
    multiple parsing of the same file.
    Allows Custodian to clear the cache after all the checks have been performed.
    """

    # Class‑level set that keeps references to all wrapped functions
    _tracked: set = set()

    def __init__(self, func: Callable) -> None:
        """
        Args:
            func: function to be decorated.
        """
        # Wrap the original function with lru_cache
        self._cached_func = functools.lru_cache()(func)
        # Store the wrapped function in the class‑level set
        self.__class__._tracked.add(self._cached_func)
        # Preserve metadata of the original function
        functools.update_wrapper(self, func)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Call the decorated function."""
        return self._cached_func(*args, **kwargs)

    @classmethod
    def tracked_cache_clear(cls) -> None:
        """Clear the cache of all the decorated functions."""
        for cached in list(cls._tracked):
            try:
                cached.cache_clear()
            except AttributeError:
                # In case the cached object does not expose cache_clear
                pass
