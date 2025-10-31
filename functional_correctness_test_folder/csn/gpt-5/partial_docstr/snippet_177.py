from functools import lru_cache, update_wrapper
import weakref


class tracked_lru_cache:
    '''
    Decorator wrapping the functools.lru_cache adding a tracking of the
    functions that have been wrapped.
    Exposes a method to clear the cache of all the wrapped functions.
    Used to cache the parsed outputs in handlers/validators, to avoid
    multiple parsing of the same file.
    Allows Custodian to clear the cache after all the checks have been performed.
    '''
    _tracked_instances = weakref.WeakSet()

    def __init__(self, func) -> None:
        cached = lru_cache(maxsize=None)(func)
        self._cached = cached
        update_wrapper(self, func)
        self.__wrapped__ = cached
        type(self)._tracked_instances.add(self)

    def __call__(self, *args, **kwargs):
        return self._cached(*args, **kwargs)

    @classmethod
    def tracked_cache_clear(cls) -> None:
        for inst in list(cls._tracked_instances):
            try:
                inst._cached.cache_clear()
            except Exception:
                pass
