class DummyFuture:
    """
    Mimics some of `concurrent.futures.Future` but runs immediately.
    """

    def __init__(self, fn, *args, **kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def result(self):
        return self.fn(*self.args, **self.kwargs)