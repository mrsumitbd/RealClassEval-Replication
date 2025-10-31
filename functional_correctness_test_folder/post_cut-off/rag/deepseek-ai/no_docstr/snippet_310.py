
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
            self._expiry_times = {}
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
                self._expiry_times[key] = time.time() + ttl
            else:
                self._expiry_times.pop(key, None)

    def get(self, key: str, default: Any = None) -> Any:
        '''Get the value associated with a key.
        Args:
            key: The key for the data within the session.
            default: The value to return if the session or key is not found.
        Returns:
            The cached value, or the default value if not found.
        '''
        with self._lock:
            if key not in self._cache:
                return default
            if key in self._expiry_times and time.time() > self._expiry_times[key]:
                del self._cache[key]
                del self._expiry_times[key]
                return default
            return self._cache.get(key, default)

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
                self._expiry_times.pop(key, None)
                return True
            return False

    def clear(self) -> bool:
        '''Remove all data.
        Returns:
            True if the data was cleared, False otherwise.
        '''
        with self._lock:
            self._cache.clear()
            self._expiry_times.clear()
            return True
