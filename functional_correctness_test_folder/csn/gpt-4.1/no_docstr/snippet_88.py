
class Cache:

    def __init__(self):
        self._store = {}

    def clear(self):
        self._store.clear()

    def get(self, key, creator):
        if key in self._store:
            return self._store[key]
        value = creator()
        self._store[key] = value
        return value
