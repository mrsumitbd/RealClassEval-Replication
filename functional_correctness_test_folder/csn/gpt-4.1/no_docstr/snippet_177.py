
from functools import wraps
from collections import OrderedDict
import threading


class tracked_lru_cache:
    _all_caches = []
    _lock = threading.Lock()

    def __init__(self, func) -> None:
        self.func = func
        self.cache = OrderedDict()
        self.maxsize = 128  # default LRU size
        wraps(func)(self)
        with tracked_lru_cache._lock:
            tracked_lru_cache._all_caches.append(self)

    def __call__(self, *args, **kwargs):
        key = args
        if kwargs:
            key += tuple(sorted(kwargs.items()))
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        result = self.func(*args, **kwargs)
        self.cache[key] = result
        self.cache.move_to_end(key)
        if len(self.cache) > self.maxsize:
            self.cache.popitem(last=False)
        return result

    @classmethod
    def tracked_cache_clear(cls) -> None:
        with cls._lock:
            for instance in cls._all_caches:
                instance.cache.clear()
