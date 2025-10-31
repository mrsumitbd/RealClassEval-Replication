from contextlib import contextmanager

class DownloadExceptionTracker:

    def __init__(self):
        self.collection_failure_exceptions = []

    @contextmanager
    def __call__(self):
        try:
            yield
        except Exception as e:
            self.collection_failure_exceptions.append(e)