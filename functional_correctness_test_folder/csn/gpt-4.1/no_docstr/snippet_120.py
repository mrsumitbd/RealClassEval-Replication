
class NestedDummyClass:
    class Inner:
        def __init__(self, value):
            self.value = value

        def get_value(self):
            return self.value

    def __init__(self):
        self._inner = self.Inner(42)

    def run(self):
        return self._inner.get_value()

    @property
    def prop(self):
        return self._inner.value
