from typing import Any, Optional, Tuple
from threading import RLock
import time


class InMemoryCache:
    '''A thread-safe Singleton class to manage cache data.
    Ensures only one instance of the cache exists across the application.
    '''

    _instance: Optional["InMemoryCache"] = None
    _class_lock: RLock = RLock()

    def __new__(cls):
        '''Override __new__ to control instance creation (Singleton pattern).
        Uses a lock to ensure thread safety during the first instantiation.
        Returns:
            The singleton instance of InMemoryCache.
        '''
        if cls._instance is None:
            with cls._class_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    # type: ignore[attr-defined]
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        '''Initialize the cache storage.
        Uses a flag (_initialized) to ensure this logic runs only on the very first
        creation of the singleton instance.
        '''
        if getattr(self, "_initialized", False):
            return
        self._data_lock = RLock()
        # Store: key -> (value, expires_at or None)
        self._store: dict[str, Tuple[Any, Optional[float]]] = {}
        self._initialized = True

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        '''Set a key-value pair.
        Args:
            key: The key for the data.
            value: The data to store.
            ttl: Time to live in seconds. If None, data will not expire.
        '''
        with self._data_lock:
            if ttl is not None and ttl <= 0:
                self._store.pop(key, None)
                return
            expires_at = None if ttl is None else (time.time() + ttl)
            self._store[key] = (value, expires_at)

    def get(self, key: str, default: Any = None) -> Any:
        '''Get the value associated with a key.
        Args:
            key: The key for the data within the session.
            default: The value to return if the session or key is not found.
        Returns:
            The cached value, or the default value if not found.
        '''
        with self._data_lock:
            item = self._store.get(key)
            if item is None:
                return default
            value, expires_at = item
            if expires_at is not None and time.time() >= expires_at:
                self._store.pop(key, None)
                return default
            return value

    def delete(self, key: str) -> bool:
        '''Delete a specific key-value pair from a cache.
        Args:
            key: The key to delete.
        Returns:
            True if the key was found and deleted, False otherwise.
        '''
        with self._data_lock:
            return self._store.pop(key, None) is not None

    def clear(self) -> bool:
        '''Remove all data.
        Returns:
            True if the data was cleared, False otherwise.
        '''
        with self._data_lock:
            had_data = bool(self._store)
            self._store.clear()
            return had_data
