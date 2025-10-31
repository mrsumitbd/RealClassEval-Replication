
from typing import Any, Optional
import time


class InMemoryCache:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InMemoryCache, cls).__new__(cls)
            cls._instance._cache = {}
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_cache'):
            self._cache = {}

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        if ttl is not None:
            expire_time = time.time() + ttl
        else:
            expire_time = None
        self._cache[key] = (value, expire_time)

    def get(self, key: str, default: Any = None) -> Any:
        if key in self._cache:
            value, expire_time = self._cache[key]
            if expire_time is None or time.time() < expire_time:
                return value
            else:
                del self._cache[key]
        return default

    def delete(self, key: str) -> None:
        if key in self._cache:
            del self._cache[key]

    def clear(self) -> bool:
        self._cache.clear()
        return True
