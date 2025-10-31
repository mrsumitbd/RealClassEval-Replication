
class SingleThing:

    def __init__(self, thing):

        self._thing = thing

    def get_thing(self, _=None):

        return self._thing

    def get_things(self):

        return [self._thing]

    def get_name(self):

        return self._thing.__class__.__name__
