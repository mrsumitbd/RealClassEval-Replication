
class LoggerBackend:

    def __init__(self, **kwargs):
        self.config = kwargs

    def send(self, event):
        raise NotImplementedError(
            "Subclasses must implement the 'send' method")
