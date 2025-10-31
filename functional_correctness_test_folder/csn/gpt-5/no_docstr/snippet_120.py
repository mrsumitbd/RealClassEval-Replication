class NestedDummyClass:
    class _Counter:
        def __init__(self, start=0):
            self.value = int(start)

        def inc(self, n=1):
            self.value += int(n)
            return self.value

        def reset(self):
            self.value = 0

        @property
        def even(self):
            return self.value % 2 == 0

    def __init__(self, start=0):
        self._counter = self._Counter(start)

    def run(self):
        return self._counter.inc()

    @property
    def prop(self):
        return {"value": self._counter.value, "even": self._counter.even}
