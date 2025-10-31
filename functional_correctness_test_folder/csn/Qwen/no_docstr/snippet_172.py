
class MultipleThings:

    def __init__(self, things, name):
        self.things = things
        self.name = name

    def get_thing(self, idx):
        if 0 <= idx < len(self.things):
            return self.things[idx]
        return None

    def get_things(self):
        return self.things

    def get_name(self):
        return self.name
