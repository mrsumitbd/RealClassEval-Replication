class NullProgressBar:
    """Progress bar API that takes no actions."""

    def __init__(self, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def update(self, _arg=None, *, completed=None):
        return