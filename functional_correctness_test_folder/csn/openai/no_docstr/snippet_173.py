class SingleThing:
    def __init__(self, thing):
        self._thing = thing

    def get_thing(self, _=None):
        return self._thing

    def get_things(self):
        return [self._thing]

    def get_name(self):
        if hasattr(self._thing, "name"):
            return self._thing.name
        return str(self._thing)
