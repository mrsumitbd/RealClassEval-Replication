
class LoggerBackend:

    def __init__(self, **kwargs):
        self.config = kwargs

    def send(self, event):
        print(f"Logging event: {event}")
