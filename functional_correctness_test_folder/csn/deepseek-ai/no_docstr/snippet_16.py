
class _Trail:

    def __init__(self, screen: Screen, x: int):
        self.screen = screen
        self.x = x
        self.segments = []

    def _maybe_reseed(self, normal: bool):
        if normal or len(self.segments) == 0:
            self.segments.append((self.x, self.screen.height))

    def update(self, reseed: bool):
        self._maybe_reseed(reseed)
        new_segments = []
        for x, y in self.segments:
            if y > 0:
                new_segments.append((x, y - 1))
        self.segments = new_segments
