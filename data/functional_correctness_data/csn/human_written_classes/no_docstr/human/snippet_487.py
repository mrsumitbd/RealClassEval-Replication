class CursorInterface:
    __slots__ = ('cursor', 'query')

    def __init__(self, cursor, query=None):
        self.cursor = cursor
        self.query = query

    def __aiter__(self):
        return CursorIterator(self.cursor.__aiter__())

    def __getattr__(self, item):
        return getattr(self.cursor, item)

    def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.query:
            self.query.__aexit(exc_type, exc_val, exc_tb)
        else:
            raise AttributeError('you shouldnt be here')