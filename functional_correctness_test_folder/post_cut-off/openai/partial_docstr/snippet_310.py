
import time
import threading
from typing import Any, Optional


class InMemoryCache:
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super(InMemoryCache, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Ensure initialization happens only once
        if getattr(self, "_initialized", False):
            return
        self._store = {}  # key -> (value, expire_at)
        self._lock = threading.RLock()
        self._initialized = True

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        expire_at = None
        if ttl is not None:
            expire_at = time.time() + ttl
        with self._lock:
            self._store[key] = (value, expire_at)

    def get(self, key: str, default: Any = None) -> Any:
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return default
            value, expire_at = entry
            if expire_at is not None and time.time() > expire_at:
                # expired
                del self._store[key]
                return default
            return value

    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self._store:
                del self._store[key]
                return True
            return False

    def clear(self) -> bool:
        with self._lock:
            if self._store:
                self._store.clear()
                return True
            return False
