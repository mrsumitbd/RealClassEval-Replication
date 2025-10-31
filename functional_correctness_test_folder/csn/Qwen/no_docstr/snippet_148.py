
class Addr:

    def __init__(self, map):
        self.map = map
        self.expiration = None

    def update(self, *args):
        if args:
            self.map.update(args[0])
        if len(args) > 1:
            self.expiration = args[1]

    def _expire(self):
        if self.expiration:
            current_time = time.time()
            if current_time > self.expiration:
                self.map.clear()
                self.expiration = None
