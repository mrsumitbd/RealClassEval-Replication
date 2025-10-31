class _CookieCacheDummy:
    """Dummy cache to use if Cookie cache is disabled"""

    def lookup(self, tkr):
        return None

    def store(self, tkr, Cookie):
        pass

    @property
    def Cookie_db(self):
        return None