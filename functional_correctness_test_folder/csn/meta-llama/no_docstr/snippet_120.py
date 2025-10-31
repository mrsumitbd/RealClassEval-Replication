
class NestedDummyClass:

    def __init__(self):
        self._prop = None

    def run(self):
        self._prop = "Property Value"
        print("Running NestedDummyClass")

    @property
    def prop(self):
        return self._prop
