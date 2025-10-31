
from functools import lru_cache
from collections import defaultdict


class tracked_lru_cache:

    _cache_stats = defaultdict(int)

    def __init__(self, func) -> None:
        self.func = func
        self.cache = lru_cache(maxsize=None)(func)

    def __call__(self, *args, **kwargs):
        result = self.cache(*args, **kwargs)
        self._cache_stats[self.func.__name__] += 1
        return result

    @classmethod
    def tracked_cache_clear(cls) -> None:
        cls._cache_stats.clear()
