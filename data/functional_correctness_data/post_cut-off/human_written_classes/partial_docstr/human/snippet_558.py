class DummyTask:
    """Dummy task that returns the data passed to it.

    Used in ImageViewer to pass data to the ImageViewer without using threads.
    """

    def __init__(self, data):
        self.data = data

    def ready(self):
        """Always returns True."""
        return True

    def get(self):
        """Gets the data passed to the DummyTask."""
        return self.data