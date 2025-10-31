
class EventInterceptor:

    def __init__(self, source, **events):
        self.source = source
        self.events = events
        self.originals = {}

    def __enter__(self):
        for event_name, handler in self.events.items():
            # Save original handler if exists
            self.originals[event_name] = getattr(self.source, event_name, None)
            setattr(self.source, event_name, handler)
        return self

    def __exit__(self, typ, value, traceback):
        for event_name, original_handler in self.originals.items():
            setattr(self.source, event_name, original_handler)
