class Devnull:
    """'Black hole' for output that should not be printed"""

    def write(self, *_):
        pass

    def flush(self, *_):
        pass