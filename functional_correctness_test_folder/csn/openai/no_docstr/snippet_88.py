class Cache:
    def __init__(self):
        self._store = {}

    def clear(self):
        self._store.clear()

    def get(self, key, creator):
        if key not in self._store:
            self._store[key] = creator()
        return self._store[key]
