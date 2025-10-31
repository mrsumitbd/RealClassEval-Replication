
import threading


class Cache:
    '''Thread-safe general purpose cache for objects.
    Add things to the cache by calling get(key, creator). If the requested key
    doesn't exist, will add the item to the cache for you.
    '''

    def __init__(self):
        self.cache = {}
        self.lock = threading.Lock()
        self.no_cache = False

    def clear(self):
        '''Clear the cache of all objects.'''
        with self.lock:
            self.cache.clear()

    def get(self, key, creator):
        '''Get key from cache. If key not exist, call creator and cache result.
        Looks for key in cache and returns object for that key.
        If key is not found, call creator and save the result to cache for that
        key.
        Be warned that get happens under the context of a Lock. . . so if
        creator takes a long time you might well be blocking.
        If config no_cache is True, bypasses cache entirely - will call
        creator each time and also not save the result to cache.
        Args:
            key: key (unique id) of cached item
            creator: callable that will create cached object if key not found
        Returns:
            Cached item at key or the result of creator()
        '''
        if self.no_cache:
            return creator()

        with self.lock:
            if key in self.cache:
                return self.cache[key]
            else:
                result = creator()
                self.cache[key] = result
                return result
