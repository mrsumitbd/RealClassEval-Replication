import threading

class ThreadNameKeeper:
    """A contect manager to get back the thread name as it was before. It
    is meant to be used when modifying the 'MainThread' tread.
    """

    def __enter__(self):
        self._name = threading.current_thread().name

    def __exit__(self, *exc_args):
        threading.current_thread().name = self._name