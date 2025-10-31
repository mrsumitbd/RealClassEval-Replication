
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
        self._source = source
        self._events = events
        self._original_handlers = {}

    def __enter__(self):
        '''Starts event interception.'''
        for event_name, new_handler in self._events.items():
            # Save the original handler
            self._original_handlers[event_name] = getattr(
                self._source, event_name)
            # Set the new handler
            setattr(self._source, event_name, new_handler)
        return self

    def __exit__(self, typ, value, traceback):
        '''Stops event interception.'''
        for event_name, original_handler in self._original_handlers.items():
            setattr(self._source, event_name, original_handler)
        self._original_handlers.clear()
