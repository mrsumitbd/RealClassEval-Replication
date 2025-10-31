class tracked_lru_cache:
    _instances = None

    def __init__(self, func) -> None:
        import threading
        from collections import OrderedDict
        import weakref

        if tracked_lru_cache._instances is None:
            tracked_lru_cache._instances = weakref.WeakSet()

        self._func = func
        self._cache = OrderedDict()
        self._lock = threading.RLock()
        self._maxsize = 128
        self.__wrapped__ = func  # for introspection
        tracked_lru_cache._instances.add(self)

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        import functools
        return functools.partial(self.__call__, obj)

    def _make_key(self, args, kwargs):
        if not kwargs:
            return ("__K__", args, None)
        try:
            items = tuple(sorted(kwargs.items()))
        except TypeError:
            # Unorderable keys; fallback to insertion order (still might be unhashable)
            items = tuple(kwargs.items())
        return ("__K__", args, items)

    def __call__(self, *args, **kwargs):
        key = None
        try:
            key = self._make_key(args, kwargs)
            hash(key)
        except Exception:
            return self.__wrapped__(*args, **kwargs)

        with self._lock:
            if key in self._cache:
                val = self._cache.pop(key)
                self._cache[key] = val
                return val

        result = self.__wrapped__(*args, **kwargs)

        with self._lock:
            # Store and enforce LRU size
            if key in self._cache:
                # Another thread may have populated it meanwhile
                self._cache.pop(key, None)
            self._cache[key] = result
            if self._maxsize is not None and self._maxsize > 0:
                while len(self._cache) > self._maxsize:
                    self._cache.popitem(last=False)
        return result

    @classmethod
    def tracked_cache_clear(cls) -> None:
        insts = list(cls._instances) if cls._instances is not None else []
        for inst in insts:
            try:
                with inst._lock:
                    inst._cache.clear()
            except Exception:
                pass
