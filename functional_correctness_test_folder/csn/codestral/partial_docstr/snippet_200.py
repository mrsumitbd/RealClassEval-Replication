
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
        return self

    def __exit__(self, typ, value, traceback):
        for event_name, handler in self.original_handlers.items():
            setattr(self.source, event_name, handler)
        self.original_handlers.clear()
