
class DummyClass:

    def __init__(self):
        self._value = None

    def run(self):
        self._value = "ran"

    @property
    def prop(self):
        return self._value
