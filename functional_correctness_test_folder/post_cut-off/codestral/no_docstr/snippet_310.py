
import time
from typing import Any, Optional


class InMemoryCache:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InMemoryCache, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'cache'):
            self.cache = {}

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        if ttl is not None:
            expiration_time = time.time() + ttl
            self.cache[key] = (value, expiration_time)
        else:
            self.cache[key] = (value, None)

    def get(self, key: str, default: Any = None) -> Any:
        if key in self.cache:
            value, expiration_time = self.cache[key]
            if expiration_time is None or expiration_time > time.time():
                return value
            else:
                del self.cache[key]
        return default

    def delete(self, key: str) -> None:
        if key in self.cache:
            del self.cache[key]

    def clear(self) -> bool:
        self.cache.clear()
        return True
