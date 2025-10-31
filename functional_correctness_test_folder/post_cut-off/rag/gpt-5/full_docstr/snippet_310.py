from typing import Any, Optional
import threading
import time


class InMemoryCache:
    '''A thread-safe Singleton class to manage cache data.
    Ensures only one instance of the cache exists across the application.
    '''
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        '''Override __new__ to control instance creation (Singleton pattern).
        Uses a lock to ensure thread safety during the first instantiation.
        Returns:
            The singleton instance of InMemoryCache.
        '''
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        '''Initialize the cache storage.
        Uses a flag (_initialized) to ensure this logic runs only on the very first
        creation of the singleton instance.
        '''
        if getattr(self, "_initialized", False):
            return
        self._cache: dict[str, tuple[Any, Optional[float]]] = {}
        self._lock = threading.RLock()
        self._initialized = True

    def _purge_expired(self) -> None:
        now = time.time()
        expired_keys = [k for k, (_, exp) in self._cache.items(
        ) if exp is not None and exp <= now]
        for k in expired_keys:
            self._cache.pop(k, None)

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        '''Set a key-value pair.
        Args:
            key: The key for the data.
            value: The data to store.
            ttl: Time to live in seconds. If None, data will not expire.
        '''
        expires_at: Optional[float] = None
        if ttl is not None:
            try:
                ttl_int = int(ttl)
            except (TypeError, ValueError):
                ttl_int = None
            if ttl_int is not None:
                if ttl_int <= 0:
                    with self._lock:
                        self._cache.pop(key, None)
                        self._purge_expired()
                    return
                expires_at = time.time() + ttl_int
        with self._lock:
            self._cache[key] = (value, expires_at)
            self._purge_expired()

    def get(self, key: str, default: Any = None) -> Any:
        '''Get the value associated with a key.
        Args:
            key: The key for the data within the session.
            default: The value to return if the session or key is not found.
        Returns:
            The cached value, or the default value if not found.
        '''
        with self._lock:
            item = self._cache.get(key)
            if item is None:
                return default
            value, expires_at = item
            if expires_at is not None and expires_at <= time.time():
                self._cache.pop(key, None)
                return default
            return value

    def delete(self, key: str) -> bool:
        '''Delete a specific key-value pair from a cache.
        Args:
            key: The key to delete.
        Returns:
            True if the key was found and deleted, False otherwise.
        '''
        with self._lock:
            existed = key in self._cache
            if existed:
                self._cache.pop(key, None)
            return existed

    def clear(self) -> bool:
        '''Remove all data.
        Returns:
            True if the data was cleared, False otherwise.
        '''
        with self._lock:
            self._cache.clear()
            return True
