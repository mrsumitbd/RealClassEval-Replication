
import functools


class tracked_lru_cache:
    def __init__(self, func):
        self.func = func
        self.cache = {}
        self.hits = 0
        self.misses = 0
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        else:
            self.misses += 1
            result = self.func(*args, **kwargs)
            self.cache[key] = result
            return result

    @classmethod
    def tracked_cache_clear(cls) -> None:
        for instance in cls.__instances:
            instance.cache.clear()
            instance.hits = 0
            instance.misses = 0

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__instances = []

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        cls.__instances.append(instance)
        return instance
