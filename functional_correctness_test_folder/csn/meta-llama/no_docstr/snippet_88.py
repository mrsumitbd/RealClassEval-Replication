
from threading import Lock


class Cache:

    def __init__(self):
        self.cache = {}
        self.lock = Lock()

    def clear(self):
        with self.lock:
            self.cache.clear()

    def get(self, key, creator):
        with self.lock:
            if key not in self.cache:
                self.cache[key] = creator()
        return self.cache[key]
