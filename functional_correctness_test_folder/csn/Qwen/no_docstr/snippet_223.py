
class LoggerBackend:

    def __init__(self, **kwargs):
        self.config = kwargs

    def send(self, event):
        # Example implementation: print the event to the console
        print(f"Logging event: {event}")
