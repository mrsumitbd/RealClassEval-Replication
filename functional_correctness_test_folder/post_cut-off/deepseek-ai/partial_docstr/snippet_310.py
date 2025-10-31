
import threading
from typing import Any, Optional
import time


class InMemoryCache:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(InMemoryCache, cls).__new__(cls)
                cls._instance._cache = {}
                cls._instance._ttl = {}
        return cls._instance

    def __init__(self):
        pass

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        self._cache[key] = value
        if ttl is not None:
            self._ttl[key] = time.time() + ttl

    def get(self, key: str, default: Any = None) -> Any:
        if key in self._cache:
            if key in self._ttl:
                if time.time() < self._ttl[key]:
                    return self._cache[key]
                else:
                    del self._cache[key]
                    del self._ttl[key]
                    return default
            else:
                return self._cache[key]
        return default

    def delete(self, key: str) -> None:
        if key in self._cache:
            del self._cache[key]
            if key in self._ttl:
                del self._ttl[key]

    def clear(self) -> bool:
        self._cache.clear()
        self._ttl.clear()
        return True
