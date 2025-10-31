class Cache:
    def __init__(self):
        import threading
        self._cache = {}
        self._lock = threading.RLock()
        self._key_locks = {}

    def clear(self):
        with self._lock:
            self._cache.clear()
            self._key_locks.clear()

    def get(self, key, creator):
        with self._lock:
            if key in self._cache:
                return self._cache[key]
            lock = self._key_locks.get(key)
            if lock is None:
                import threading
                lock = threading.Lock()
                self._key_locks[key] = lock

        with lock:
            with self._lock:
                if key in self._cache:
                    return self._cache[key]
            value = creator()
            with self._lock:
                self._cache[key] = value
                # Optional: cleanup per-key lock to avoid growth
                self._key_locks.pop(key, None)
            return value
