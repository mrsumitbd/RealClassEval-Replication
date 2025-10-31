
from __future__ import annotations

import time
from typing import Any, Optional, Dict, Tuple


class InMemoryCache:
    _instance: "InMemoryCache" | None = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Initialize storage and lock only once
            cls._instance._cache: Dict[str, Tuple[Any, Optional[float]]] = {}
            cls._instance._lock = None  # will be set in __init__
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        # Simple lock for thread safety
        import threading

        self._lock = threading.RLock()
        self._initialized = True

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Store a value with an optional TTL (seconds)."""
        expiry = time.time() + ttl if ttl is not None else None
        with self._lock:
            self._cache[key] = (value, expiry)

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a value, returning default if missing or expired."""
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                return default
            value, expiry = entry
            if expiry is not None and time.time() > expiry:
                # expired
                del self._cache[key]
                return default
            return value

    def delete(self, key: str) -> None:
        """Remove a key from the cache if it exists."""
        with self._lock:
            self._cache.pop(key, None)

    def clear(self) -> bool:
        """Clear all entries from the cache."""
        with self._lock:
            self._cache.clear()
        return True
