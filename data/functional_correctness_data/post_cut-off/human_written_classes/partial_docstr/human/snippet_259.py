import weakref

class Cleanupper:
    """
    Utility class to call cleanup functions at the end of the __main__ scope. Similar functionality to
    atexit but called before Python starts tearing down objects/threads.
    """

    def __init__(self):
        self.atexit_fns = []
        weakref.finalize(self, self._shutdown)

    def register_atexit(self, fn):
        self.atexit_fns.append(fn)

    def unregister_atexit(self, fn):
        if fn in self.atexit_fns:
            self.atexit_fns.remove(fn)

    def _shutdown(self):
        for fn in self.atexit_fns:
            fn()
        self.atexit_fns = []