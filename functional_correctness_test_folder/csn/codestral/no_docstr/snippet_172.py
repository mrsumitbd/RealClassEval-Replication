
class MultipleThings:

    def __init__(self, things, name):

        self.things = things
        self.name = name

    def get_thing(self, idx):

        return self.things[idx]

    def get_things(self):

        return self.things

    def get_name(self):

        return self.name
