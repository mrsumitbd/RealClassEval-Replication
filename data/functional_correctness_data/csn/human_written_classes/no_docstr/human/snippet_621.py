class Trigger:

    def __init__(self):
        self._callbacks = set()

    def add_callback(self, f):
        self._callbacks.add(f)
        f()

    def remove_callback(self, f):
        self._callbacks.remove(f)

    def fire(self):
        for f in self._callbacks:
            f()