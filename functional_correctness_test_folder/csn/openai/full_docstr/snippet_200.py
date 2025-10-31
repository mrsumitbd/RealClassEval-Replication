
class EventInterceptor:
    '''A context object helping to temporarily intercept
    a set of events on an object exposing a set of event hooks.
    '''

    def __init__(self, source, **events):
        '''
        Constructor.
        :param source: the object exposing a set of event hook properies
        :param events: a set of event_hook_name=event_handler pairs specifying
                       which events to intercept.
        '''
        self.source = source
        self.events = events
        self._original_handlers = {}

    def __enter__(self):
        '''Starts event interception.'''
        for name, handler in self.events.items():
            # Store the original handler (could be None)
            self._original_handlers[name] = getattr(self.source, name, None)
            # Replace with the new handler
            setattr(self.source, name, handler)
        return self

    def __exit__(self, typ, value, traceback):
        '''Stops event interception.'''
        for name, original in self._original_handlers.items():
            if original is None:
                # Remove the attribute if it didn't exist before
                if hasattr(self.source, name):
                    delattr(self.source, name)
            else:
                setattr(self.source, name, original)
        # Clear stored originals to avoid accidental reuse
        self._original_handlers.clear()
        # Returning False propagates exceptions, if any
        return False
