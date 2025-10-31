
import random


class _Trail:

    def __init__(self, screen: 'Screen', x: int):
        self.screen = screen
        self.x = x
        self.y = 0
        self.length = 10
        self.trail = [(self.x, y) for y in range(self.y, self.y + self.length)]
        self.reseed_interval = 100
        self.steps = 0

    def _maybe_reseed(self, normal: bool):
        if normal:
            self.reseed_interval = 100
        else:
            self.reseed_interval = 50
        if self.steps % self.reseed_interval == 0:
            self._reseed()

    def _reseed(self):
        self.y = random.randint(0, self.screen.height - self.length)
        self.trail = [(self.x, y) for y in range(self.y, self.y + self.length)]

    def update(self, reseed: bool):
        self.steps += 1
        self._maybe_reseed(reseed)
        self.y = (self.y + 1) % self.screen.height
        self.trail = [(self.x, (y + 1) % self.screen.height)
                      for y in range(self.y, self.y + self.length)]
        self._draw()

    def _draw(self):
        for point in self.trail:
            self.screen.draw_point(point)
