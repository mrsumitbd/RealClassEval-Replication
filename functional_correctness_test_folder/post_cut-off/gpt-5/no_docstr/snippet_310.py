from typing import Any, Optional
import time
import threading


class InMemoryCache:
    _instance = None
    _lock = threading.RLock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self._store: dict[str, tuple[Any, Optional[float]]] = {}
        self._initialized = True

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        with self._lock:
            expires_at: Optional[float]
            if ttl is None:
                expires_at = None
            else:
                now = time.time()
                expires_at = now + ttl if ttl > 0 else now
            self._store[key] = (value, expires_at)

    def get(self, key: str, default: Any = None) -> Any:
        with self._lock:
            item = self._store.get(key)
            if item is None:
                return default
            value, expires_at = item
            if expires_at is not None and expires_at <= time.time():
                self._store.pop(key, None)
                return default
            return value

    def delete(self, key: str) -> None:
        with self._lock:
            self._store.pop(key, None)

    def clear(self) -> bool:
        with self._lock:
            self._store.clear()
        return True
