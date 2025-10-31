
class SingleThing:

    def __init__(self, thing):
        self.thing = thing

    def get_thing(self, _=None):
        return self.thing

    def get_things(self):
        return [self.thing]

    def get_name(self):
        return self.thing
