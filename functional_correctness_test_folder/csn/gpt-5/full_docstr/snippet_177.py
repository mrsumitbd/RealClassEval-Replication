import functools
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
        '''
        Args:
            func: function to be decorated.
        '''
        self._func = func
        self._cached = functools.lru_cache(maxsize=None)(func)
        # Copy metadata for nicer introspection
        functools.update_wrapper(self, func)
        type(self)._tracked_instances.add(self)

    def __call__(self, *args, **kwargs):
        '''Call the decorated function.'''
        return self._cached(*args, **kwargs)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        # Bind instance as first argument for method usage
        return functools.partial(self.__call__, instance)

    @classmethod
    def tracked_cache_clear(cls) -> None:
        '''Clear the cache of all the decorated functions.'''
        for inst in list(cls._tracked_instances):
            try:
                inst._cached.cache_clear()
            except Exception:
                pass
