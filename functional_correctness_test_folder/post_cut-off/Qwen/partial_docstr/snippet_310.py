
import threading
from typing import Any, Optional, Dict
import time


class InMemoryCache:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(InMemoryCache, cls).__new__(cls)
                cls._instance._cache = {}
                cls._instance._expirations = {}
        return cls._instance

    def __init__(self):
        pass

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        self._cache[key] = value
        if ttl is not None:
            self._expirations[key] = time.time() + ttl
        else:
            self._expirations.pop(key, None)

    def get(self, key: str, default: Any = None) -> Any:
        if key in self._cache:
            if key in self._expirations and self._expirations[key] < time.time():
                self.delete(key)
                return default
            return self._cache[key]
        return default

    def delete(self, key: str) -> bool:
        if key in self._cache:
            del self._cache[key]
            self._expirations.pop(key, None)
            return True
        return False

    def clear(self) -> bool:
        if self._cache:
            self._cache.clear()
            self._expirations.clear()
            return True
        return False
