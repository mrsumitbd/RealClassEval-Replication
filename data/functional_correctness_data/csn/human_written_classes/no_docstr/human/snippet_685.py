import time

class RequestCache:

    def __init__(self, valid_time=60):
        self._valid_time = valid_time
        self._cache = {}

    def put(self, key, value):
        self._cache[key] = {'time': time.time(), 'value': value}

    def remove(self, key):
        if key in self._cache:
            del self._cache[key]

    def get(self, key):
        if key not in self._cache:
            raise RequestCacheMissingException()
        if time.time() > self._cache[key]['time'] + self._valid_time:
            self.remove(key)
            raise RequestCacheInvalidException()
        return self._cache[key]['value']