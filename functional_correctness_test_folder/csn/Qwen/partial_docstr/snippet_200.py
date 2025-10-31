
class EventInterceptor:

    def __init__(self, source, **events):
        self.source = source
        self.events = events
        self.original_handlers = {}

    def __enter__(self):
        for event_name, handler in self.events.items():
            if hasattr(self.source, event_name):
                self.original_handlers[event_name] = getattr(
                    self.source, event_name)
                setattr(self.source, event_name, handler)

    def __exit__(self, typ, value, traceback):
        for event_name, original_handler in self.original_handlers.items():
            setattr(self.source, event_name, original_handler)
