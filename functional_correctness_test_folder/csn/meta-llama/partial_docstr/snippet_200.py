
class EventInterceptor:

    def __init__(self, source, **events):
        '''
        Constructor.
        :param source: the object exposing a set of event hook properties
        :param events: a set of event_hook_name=event_handler pairs specifying
                       which events to intercept.
        '''
        self.source = source
        self.events = events
        self.original_handlers = {}

    def __enter__(self):
        for event_name, handler in self.events.items():
            if hasattr(self.source, event_name):
                original_handler = getattr(self.source, event_name)
                self.original_handlers[event_name] = original_handler
                setattr(self.source, event_name, handler)
        return self

    def __exit__(self, typ, value, traceback):
        for event_name, original_handler in self.original_handlers.items():
            setattr(self.source, event_name, original_handler)
