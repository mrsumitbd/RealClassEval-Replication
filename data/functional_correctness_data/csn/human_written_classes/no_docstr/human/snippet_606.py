class _Coro:
    __slots__ = ('_it',)

    def __init__(self, it):
        self._it = it

    def __await__(self):
        return self._it