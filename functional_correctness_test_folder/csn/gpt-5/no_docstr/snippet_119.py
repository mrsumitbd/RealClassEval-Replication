class DummyClass:
    def __init__(self, start: int = 0):
        self._value = int(start)

    def run(self):
        self._value += 1
        return self._value

    @property
    def prop(self):
        return self._value
