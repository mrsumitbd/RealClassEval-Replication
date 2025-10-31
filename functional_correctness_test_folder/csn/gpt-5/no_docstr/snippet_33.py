class ExceptionHandler:
    def __init__(self, exc_types=None, handler=None):
        if exc_types is None:
            exc_types = (Exception,)
        elif isinstance(exc_types, type):
            exc_types = (exc_types,)
        else:
            exc_types = tuple(exc_types)
        self._exc_types = exc_types
        if handler is not None and not callable(handler):
            raise TypeError("handler must be callable")
        self._handler = handler

    def wants(self, exc):
        if exc is None:
            return False
        if isinstance(exc, BaseException):
            return isinstance(exc, self._exc_types)
        if isinstance(exc, type) and issubclass(exc, BaseException):
            return any(issubclass(exc, t) for t in self._exc_types)
        return False

    def handle(self, exc):
        if not self.wants(exc):
            return None
        if self._handler is None:
            return exc
        return self._handler(exc)
