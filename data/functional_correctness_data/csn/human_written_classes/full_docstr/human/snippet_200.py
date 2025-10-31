class EventInterceptor:
    """A context object helping to temporarily intercept
    a set of events on an object exposing a set of event hooks.

    """

    def __init__(self, source, **events):
        """
        Constructor.

        :param source: the object exposing a set of event hook properies
        :param events: a set of event_hook_name=event_handler pairs specifying
                       which events to intercept.
        """
        self.source = source
        self.events = events

    def __enter__(self):
        """Starts event interception."""
        source = self.source
        for name, handler in self.events.items():
            hook = getattr(source, name)
            hook.subscribe(handler)

    def __exit__(self, typ, value, traceback):
        """Stops event interception."""
        source = self.source
        for name, handler in self.events.items():
            hook = getattr(source, name)
            hook.unsubscribe(handler)