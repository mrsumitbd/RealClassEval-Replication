from collections import OrderedDict

class LRUCache:

    def __init__(self, size):
        self.size = size
        self.lru_cache = OrderedDict()

    def get(self, key):
        try:
            value = self.lru_cache.pop(key)
            self.lru_cache[key] = value
            return value
        except KeyError:
            return -1

    def put(self, key, value):
        try:
            self.lru_cache.pop(key)
        except KeyError:
            if len(self.lru_cache) >= self.size:
                self.lru_cache.popitem(last=False)
        self.lru_cache[key] = value