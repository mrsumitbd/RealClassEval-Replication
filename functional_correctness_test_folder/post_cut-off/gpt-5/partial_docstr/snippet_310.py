from typing import Any, Optional
import time
import threading


class InMemoryCache:
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
        if getattr(self, "_initialized", False):
            return
        self._store: dict[str, tuple[Any, Optional[float]]] = {}
        self._lock = threading.RLock()
        self._initialized = True

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        expires_at: Optional[float] = None
        if ttl is not None:
            if ttl <= 0:
                with self._lock:
                    self._store.pop(key, None)
                return
            expires_at = time.time() + float(ttl)
        with self._lock:
            self._store[key] = (value, expires_at)

    def get(self, key: str, default: Any = None) -> Any:
        '''Get the value associated with a key.
        Args:
            key: The key for the data within the session.
            default: The value to return if the session or key is not found.
        Returns:
            The cached value, or the default value if not found.
        '''
        now = time.time()
        with self._lock:
            item = self._store.get(key)
            if item is None:
                return default
            value, expires_at = item
            if expires_at is not None and expires_at <= now:
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
        with self._lock:
            return self._store.pop(key, None) is not None

    def clear(self) -> bool:
        '''Remove all data.
        Returns:
            True if the data was cleared, False otherwise.
        '''
        with self._lock:
            had_data = bool(self._store)
            self._store.clear()
            return had_data
