
class _Trail:

    def __init__(self, screen: Screen, x: int):

        self.screen = screen
        self.x = x
        self.y = 0
        self.length = 0
        self.max_length = 100
        self.color = (255, 255, 255)
        self.points = []

    def _maybe_reseed(self, normal: bool):

        if normal:
            self.y = 0
            self.length = 0
            self.points = []
        else:
            self.y = self.screen.height - 1
            self.length = 0
            self.points = []

    def update(self, reseed: bool):

        if reseed:
            self._maybe_reseed(True)
        else:
            self.y += 1
            self.length += 1
            self.points.append((self.x, self.y))
            if self.length > self.max_length:
                self.points.pop(0)
