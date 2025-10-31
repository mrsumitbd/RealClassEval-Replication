
class Addr:

    def __init__(self, map):
        self.map = map

    def update(self, *args):
        for key, value in args:
            self.map[key] = value

    def _expire(self):
        self.map.clear()
