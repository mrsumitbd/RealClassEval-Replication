class EventInterceptor:

    def __init__(self, source, **events):
        self._source = source
        self._events = dict(events)
        self._originals = {}
        self._active = False

    def __enter__(self):
        if self._active:
            return self
        self._originals = {}
        for name, handler in self._events.items():
            existed = hasattr(self._source, name)
            original = getattr(self._source, name) if existed else None
            self._originals[name] = (existed, original)
            setattr(self._source, name, handler)
        self._active = True
        return self

    def __exit__(self, typ, value, traceback):
        if not self._active:
            return False
        try:
            for name, (existed, original) in self._originals.items():
                if existed:
                    setattr(self._source, name, original)
                else:
                    if hasattr(self._source, name):
                        delattr(self._source, name)
        finally:
            self._active = False
            self._originals = {}
        return False
