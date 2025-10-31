class _TzCacheManager:
    _tz_cache = None

    @classmethod
    def get_tz_cache(cls):
        if cls._tz_cache is None:
            with _cache_init_lock:
                cls._initialise()
        return cls._tz_cache

    @classmethod
    def _initialise(cls, cache_dir=None):
        cls._tz_cache = _TzCache()