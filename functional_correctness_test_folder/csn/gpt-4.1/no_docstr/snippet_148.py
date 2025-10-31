
class Addr:

    def __init__(self, map):
        self.map = dict(map)
        self.expired = False

    def update(self, *args):
        if self.expired:
            raise RuntimeError("Address expired")
        for d in args:
            self.map.update(d)

    def _expire(self):
        self.expired = True
        self.map.clear()
