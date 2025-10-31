
from typing import Any, Optional
import time


class InMemoryCache:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InMemoryCache, cls).__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __init__(self):
        self._cache = {}

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        expire_time = time.time() + ttl if ttl is not None else None
        self._cache[key] = (value, expire_time)

    def get(self, key: str, default: Any = None) -> Any:
        if key not in self._cache:
            return default
        value, expire_time = self._cache[key]
        if expire_time is not None and time.time() > expire_time:
            del self._cache[key]
            return default
        return value

    def delete(self, key: str) -> None:
        if key in self._cache:
            del self._cache[key]

    def clear(self) -> bool:
        self._cache.clear()
        return True
