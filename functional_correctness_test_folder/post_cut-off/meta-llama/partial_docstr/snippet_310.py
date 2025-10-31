
import threading
from typing import Any, Optional
import time


class InMemoryCache:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(InMemoryCache, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_cache'):
            self._cache = {}
            self._expirations = {}

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        self._cache[key] = value
        if ttl is not None:
            self._expirations[key] = time.time() + ttl
        else:
            self._expirations[key] = float('inf')

    def get(self, key: str, default: Any = None) -> Any:
        if key in self._cache:
            if time.time() < self._expirations[key]:
                return self._cache[key]
            else:
                del self._cache[key]
                del self._expirations[key]
        return default

    def delete(self, key: str) -> None:
        if key in self._cache:
            del self._cache[key]
            del self._expirations[key]

    def clear(self) -> bool:
        self._cache.clear()
        self._expirations.clear()
        return True


# Example usage:
if __name__ == "__main__":
    cache = InMemoryCache()
    cache.set('test_key', 'test_value', ttl=10)
    print(cache.get('test_key'))  # prints: test_value
    cache.delete('test_key')
    print(cache.get('test_key'))  # prints: None
    cache.set('test_key', 'test_value')
    cache.clear()
    print(cache.get('test_key'))  # prints: None
