class _ScandirIter:
    """
    For compatibility with different python versions.
    Pathlib:
    - prior 3.8 - Use it as an iterator
    - 3.8 - Use it as an context manager
    """

    def __init__(self, iterator):
        self.iterator = iterator

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __iter__(self):
        return self.iterator