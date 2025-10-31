
class EventInterceptor:

    def __init__(self, source, **events):
        self.source = source
        self.events = events
        self.original_handlers = {}

    def __enter__(self):
        for event, handler in self.events.items():
            if hasattr(self.source, event):
                self.original_handlers[event] = getattr(self.source, event)
                setattr(self.source, event, handler)

    def __exit__(self, typ, value, traceback):
        for event, original_handler in self.original_handlers.items():
            setattr(self.source, event, original_handler)
