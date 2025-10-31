
class Cache:

    def __init__(self):
        self._cache = {}

    def clear(self):
        self._cache.clear()

    def get(self, key, creator):
        if key not in self._cache:
            self._cache[key] = creator()
        return self._cache[key]
