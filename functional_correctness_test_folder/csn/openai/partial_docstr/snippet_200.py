class EventInterceptor:
    def __init__(self, source, **events):
        """
        Constructor.
        :param source: the object exposing a set of event hook properties
        :param events: a set of event_hook_name=event_handler pairs specifying
                       which events to intercept.
        """
        self.source = source
        self.events = events
        self._originals = {}

    def __enter__(self):
        # Store original handlers and replace with new ones
        for name, handler in self.events.items():
            # Save the original attribute (could be None)
            self._originals[name] = getattr(self.source, name, None)
            setattr(self.source, name, handler)
        return self

    def __exit__(self, typ, value, traceback):
        # Restore original handlers
        for name, original in self._originals.items():
            setattr(self.source, name, original)
        # Clear stored originals
        self._originals.clear()
        # Do not suppress exceptions
        return False
