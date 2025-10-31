
import random


class _Flake:

    def __init__(self, screen):
        self.screen = screen
        self._reseed()

    def _reseed(self):
        self.x = random.randint(0, self.screen.width - 1)
        self.y = 0
        self.speed = random.uniform(0.5, 2.0)

    def update(self, reseed: bool):
        if reseed or self.y >= self.screen.height:
            self._reseed()
        else:
            self.y += self.speed
