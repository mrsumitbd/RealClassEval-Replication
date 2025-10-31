class _CookieCacheManager:
    _Cookie_cache = None

    @classmethod
    def get_cookie_cache(cls):
        if cls._Cookie_cache is None:
            with _cache_init_lock:
                cls._initialise()
        return cls._Cookie_cache

    @classmethod
    def _initialise(cls, cache_dir=None):
        cls._Cookie_cache = _CookieCache()