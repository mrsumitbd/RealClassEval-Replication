
from functools import lru_cache, wraps


class tracked_lru_cache:
    _tracked_caches = set()

    def __init__(self, func) -> None:
        self.func = lru_cache()(func)
        self.__class__._tracked_caches.add(self)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    @classmethod
    def tracked_cache_clear(cls) -> None:
        for cache in cls._tracked_caches:
            cache.func.cache_clear()
