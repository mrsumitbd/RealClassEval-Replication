class RemoteException:
    """Pickling wrapper for exceptions in remote process."""

    def __init__(self, exception, traceback):
        self.exception = exception
        self.traceback = traceback

    def __reduce__(self):
        return (self.rebuild_exception, (self.exception, self.traceback))

    @staticmethod
    def rebuild_exception(exception, traceback):
        try:
            exception.traceback = traceback
            exception.__cause__ = RemoteTraceback(traceback)
        except AttributeError:
            pass
        return exception