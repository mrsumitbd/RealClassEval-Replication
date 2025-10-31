class _cache_readonly:
    """
    Decorator for CachedAttribute
    """

    def __init__(self, cachename=None, resetlist=None):
        self.func = None
        self.cachename = cachename
        self.resetlist = resetlist or None

    def __call__(self, func):
        return CachedAttribute(func, cachename=self.cachename, resetlist=self.resetlist)