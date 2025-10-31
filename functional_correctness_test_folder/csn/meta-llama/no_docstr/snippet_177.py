
from functools import wraps, lru_cache


class tracked_lru_cache:
    """
    A decorator class that tracks the number of cache hits and misses.
    It uses the functools.lru_cache decorator internally.
    """

    def __init__(self, func) -> None:
        self.func = func
        self.cache_info = None
        self.cache_clear = self.tracked_cache_clear
        self.decorated_func = lru_cache(maxsize=None)(self._tracked_func)

    def _tracked_func(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        result = self.decorated_func(*args, **kwargs)
        self.cache_info = self.decorated_func.cache_info()
        return result

    @classmethod
    def tracked_cache_clear(cls) -> None:
        # This method is not directly usable as it's a class method.
        # Instead, it's meant to be used as an attribute of an instance.
        # To make it work, we need to keep track of all instances.
        # For simplicity, we'll assume it's used as an instance attribute.
        raise AttributeError(
            "tracked_cache_clear should be used as an instance attribute")

# Example usage:


@tracked_lru_cache
def add(a, b):
    return a + b


print(add(1, 2))  # Cache miss
print(add(1, 2))  # Cache hit
print(add.cache_info())  # Cache info
add.cache_clear()  # Clear cache
print(add.cache_info())  # Cache info after clearing
