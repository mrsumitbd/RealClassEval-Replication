
import functools
from typing import Callable, Any, Set


class tracked_lru_cache:
    """
    Decorator that wraps a function with ``functools.lru_cache`` and keeps a
    registry of all wrapped functions.  The registry can be cleared with
    :meth:`tracked_cache_clear`, which calls ``cache_clear`` on each cached
    function.
    """

    # Registry of all cached functions
    _tracked: Set[Callable] = set()

    def __init__(self, func: Callable) -> None:
        # Store the original function
        self._func = func
        # Create the cached version
        self._cached = functools.lru_cache(maxsize=None)(func)
        # Register the cached function
        self.__class__._tracked.add(self._cached)

        # Preserve function metadata
        functools.update_wrapper(self, func)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self._cached(*args, **kwargs)

    @classmethod
    def tracked_cache_clear(cls) -> None:
        """
        Clears the cache of all functions that have been wrapped by
        :class:`tracked_lru_cache`.
        """
        for cached_func in list(cls._tracked):
            try:
                cached_func.cache_clear()
            except AttributeError:
                # In case the cached function does not expose cache_clear
                pass
