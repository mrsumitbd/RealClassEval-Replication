class EventInterceptor:

    def __init__(self, source, **events):
        '''
        Constructor.
        :param source: the object exposing a set of event hook properies
        :param events: a set of event_hook_name=event_handler pairs specifying
                       which events to intercept.
        '''
        self._source = source
        self._events_map = {}
        self._attached = []
        for name, handlers in events.items():
            if handlers is None:
                continue
            if isinstance(handlers, (list, tuple, set)):
                flat = [h for h in handlers if h is not None]
            else:
                flat = [handlers]
            if flat:
                self._events_map[name] = flat

    def __enter__(self):
        for name, handlers in self._events_map.items():
            hook = getattr(self._source, name)
            for handler in handlers:
                self._attach(hook, handler)
                self._attached.append((hook, handler))
        return self

    def __exit__(self, typ, value, traceback):
        # Detach in reverse order of attachment
        for hook, handler in reversed(self._attached):
            try:
                self._detach(hook, handler)
            except Exception:
                pass
        self._attached.clear()
        return False

    @staticmethod
    def _attach(hook, handler):
        try:
            hook += handler
            return
        except Exception:
            pass
        # Try common APIs
        for method in ("connect", "add", "append", "subscribe", "attach"):
            m = getattr(hook, method, None)
            if callable(m):
                m(handler)
                return
        raise TypeError("Unsupported event hook type for attaching handler")

    @staticmethod
    def _detach(hook, handler):
        try:
            hook -= handler
            return
        except Exception:
            pass
        # Try common APIs
        for method in ("disconnect", "remove", "unsubscribe", "detach", "discard"):
            m = getattr(hook, method, None)
            if callable(m):
                try:
                    m(handler)
                except TypeError:
                    # Some remove-like methods don't take an argument
                    m()
                return
        raise TypeError("Unsupported event hook type for detaching handler")
