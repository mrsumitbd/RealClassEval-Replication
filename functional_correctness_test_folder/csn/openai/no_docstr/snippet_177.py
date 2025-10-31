
import collections
import functools
import weakref
from typing import Any, Callable, Tuple, FrozenSet


class tracked_lru_cache:
    """
    A simple LRU cache decorator that tracks hits and misses.
    The cache is unlimited in size unless a maxsize is specified.
    """

    # Registry of all decorator instances for global clearing
    _instances = weakref.WeakSet()

    def __init__(self, func: Callable) -> None:
        if not callable(func):
            raise TypeError("tracked_lru_cache can only decorate callables")
        self._func = func
        self._cache: "collections.OrderedDict[Tuple[Any, FrozenSet[Tuple[Any, Any]]], Any]" = collections.OrderedDict(
        )
        self.hits: int = 0
        self.misses: int = 0
        # Preserve function metadata
        functools.update_wrapper(self, func)
        # Register instance
        self._instances.add(self)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        # Build a hashable key from args and kwargs
        key = (args, frozenset(kwargs.items()))
        if key in self._cache:
            # Cache hit: move to end to mark as recently used
            self._cache.move_to_end(key)
            self.hits += 1
            return self._cache[key]
        # Cache miss: compute value and store
        result = self._func(*args, **kwargs)
        self._cache[key] = result
        self._cache.move_to_end(key)
        self.misses += 1
        return result

    @classmethod
    def tracked_cache_clear(cls) -> None:
        """
        Clear the cache and reset hit/miss counters for all tracked_lru_cache instances.
        """
        for instance in list(cls._instances):
            instance._cache.clear()
            instance.hits = 0
            instance.misses = 0
