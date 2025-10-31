class MultipleThings:

    def __init__(self, things, name):
        self._things = things
        self._name = name

    def get_thing(self, idx):
        return self._things[idx]

    def get_things(self):
        return self._things

    def get_name(self):
        return self._name
