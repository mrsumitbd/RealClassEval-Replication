class ProtectedPipe:
    """Wrapper to protect a pipe from being closed."""

    def __init__(self, pipe):
        self.pipe = pipe

    def fileno(self):
        return self.pipe.fileno()

    def close(self):
        pass