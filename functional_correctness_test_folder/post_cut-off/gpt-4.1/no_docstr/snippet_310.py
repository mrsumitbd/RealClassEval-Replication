
from typing import Any, Optional
import time
import threading


class InMemoryCache:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(InMemoryCache, cls).__new__(cls)
                    cls._instance._cache = {}
                    cls._instance._cache_lock = threading.Lock()
        return cls._instance

    def __init__(self):
        pass

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        expire_at = time.time() + ttl if ttl is not None else None
        with self._cache_lock:
            self._cache[key] = (value, expire_at)

    def get(self, key: str, default: Any = None) -> Any:
        with self._cache_lock:
            item = self._cache.get(key, None)
            if item is None:
                return default
            value, expire_at = item
            if expire_at is not None and time.time() > expire_at:
                del self._cache[key]
                return default
            return value

    def delete(self, key: str) -> None:
        with self._cache_lock:
            if key in self._cache:
                del self._cache[key]

    def clear(self) -> bool:
        with self._cache_lock:
            self._cache.clear()
        return True
