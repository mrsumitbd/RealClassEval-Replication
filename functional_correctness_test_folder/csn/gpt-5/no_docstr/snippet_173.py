class SingleThing:

    def __init__(self, thing):
        self._thing = thing

    def get_thing(self, _=None):
        return self._thing

    def get_things(self):
        return [self._thing]

    def get_name(self):
        t = self._thing
        if hasattr(t, 'get_name') and callable(getattr(t, 'get_name')):
            try:
                return t.get_name()
            except Exception:
                pass
        if hasattr(t, 'name'):
            try:
                return t.name
            except Exception:
                pass
        if hasattr(t, '__name__'):
            return t.__name__
        return str(t)
