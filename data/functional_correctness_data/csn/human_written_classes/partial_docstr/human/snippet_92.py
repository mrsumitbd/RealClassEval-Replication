class Cache:
    """Wrapper around werkzeug's cache class, to make it compatible to
    uWSGI's cache framework.
    """

    def __init__(self, cache):
        self.cache = cache

    def get(self, cache, key):
        return self.cache.get(key)

    def set(self, cache, key, value):
        return self.cache.set(key, value)

    def delete(self, cache, key):
        return self.cache.delete(key)