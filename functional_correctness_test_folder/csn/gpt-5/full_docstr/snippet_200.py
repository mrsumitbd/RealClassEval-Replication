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
        self._events = dict(events)
        self._originals = {}
        self._entered = False

    def __enter__(self):
        '''Starts event interception.'''
        if self._entered:
            return self
        applied = []
        try:
            for name, handler in self._events.items():
                original = getattr(self._source, name)
                self._originals[name] = original
                setattr(self._source, name, handler)
                applied.append(name)
            self._entered = True
            return self
        except Exception:
            # rollback any changes already applied
            for name in reversed(applied):
                try:
                    setattr(self._source, name, self._originals[name])
                except Exception:
                    pass
            self._originals.clear()
            raise

    def __exit__(self, typ, value, traceback):
        '''Stops event interception.'''
        if self._entered:
            for name, original in self._originals.items():
                try:
                    setattr(self._source, name, original)
                except Exception:
                    pass
            self._originals.clear()
            self._entered = False
        return False
