
import threading
from typing import Any, Optional
import time


class InMemoryCache:
    '''A thread-safe Singleton class to manage cache data.
    Ensures only one instance of the cache exists across the application.
    '''

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        '''Override __new__ to control instance creation (Singleton pattern).
        Uses a lock to ensure thread safety during the first instantiation.
        Returns:
            The singleton instance of InMemoryCache.
        '''
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(InMemoryCache, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        '''Initialize the cache storage.
        Uses a flag (_initialized) to ensure this logic runs only on the very first
        creation of the singleton instance.
        '''
        if not hasattr(self, '_initialized'):
            self._cache = {}
            self._expirations = {}
            self._initialized = True

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        '''Set a key-value pair.
        Args:
            key: The key for the data.
            value: The data to store.
            ttl: Time to live in seconds. If None, data will not expire.
        '''
        with self._lock:
            self._cache[key] = value
            if ttl is not None:
                self._expirations[key] = time.time() + ttl
            else:
                self._expirations.pop(key, None)

    def get(self, key: str, default: Any = None) -> Any:
        '''Get the value associated with a key.
        Args:
            key: The key for the data within the session.
            default: The value to return if the session or key is not found.
        Returns:
            The cached value, or the default value if not found.
        '''
        with self._lock:
            if key in self._cache:
                if key in self._expirations and self._expirations[key] < time.time():
                    self.delete(key)
                    return default
                return self._cache[key]
            return default

    def delete(self, key: str) -> None:
        '''Delete a specific key-value pair from a cache.
        Args:
            key: The key to delete.
        Returns:
            True if the key was found and deleted, False otherwise.
        '''
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                self._expirations.pop(key, None)

    def clear(self) -> bool:
        '''Remove all data.
        Returns:
            True if the data was cleared, False otherwise.
        '''
        with self._lock:
            self._cache.clear()
            self._expirations.clear()
            return True
