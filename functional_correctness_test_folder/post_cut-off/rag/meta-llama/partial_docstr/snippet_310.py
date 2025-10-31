
from threading import Lock
from typing import Any, Optional


class InMemoryCache:
    """A thread-safe Singleton class to manage cache data.
    Ensures only one instance of the cache exists across the application.
    """
    _instance = None
    _lock = Lock()

    def __new__(cls):
        """Override __new__ to control instance creation (Singleton pattern).
        Uses a lock to ensure thread safety during the first instantiation.
        Returns:
            The singleton instance of InMemoryCache.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(InMemoryCache, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the cache storage.
        Uses a flag (_initialized) to ensure this logic runs only on the very first
        creation of the singleton instance.
        """
        if not hasattr(self, '_initialized'):
            self._cache = {}
            self._initialized = True

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a key-value pair.
        Args:
            key: The key for the data.
            value: The data to store.
            ttl: Time to live in seconds. If None, data will not expire.
        """
        self._cache[key] = (value, ttl)

    def get(self, key: str, default: Any = None) -> Any:
        """Get the value associated with a key.
        Args:
            key: The key for the data within the session.
            default: The value to return if the session or key is not found.
        Returns:
            The cached value, or the default value if not found.
        """
        value, ttl = self._cache.get(key, (default, None))
        return value

    def delete(self, key: str) -> None:
        """Delete a specific key-value pair from a cache.
        Args:
            key: The key to delete.
        """
        if key in self._cache:
            del self._cache[key]

    def clear(self) -> bool:
        """Remove all data.
        Returns:
            True if the data was cleared, False otherwise.
        """
        self._cache.clear()
        return True
