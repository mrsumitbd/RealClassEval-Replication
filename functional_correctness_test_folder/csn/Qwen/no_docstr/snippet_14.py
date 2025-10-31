
import random


class _Flake:

    def __init__(self, screen: 'Screen'):
        self.screen = screen
        self.x = random.randint(0, screen.width)
        self.y = random.randint(0, screen.height)
        self.size = random.randint(1, 3)
        self.speed = random.uniform(0.5, 2.0)

    def _reseed(self):
        self.x = random.randint(0, self.screen.width)
        self.y = random.randint(0, self.screen.height)
        self.size = random.randint(1, 3)
        self.speed = random.uniform(0.5, 2.0)

    def update(self, reseed: bool):
        if reseed:
            self._reseed()
        else:
            self.y += self.speed
            if self.y > self.screen.height:
                self.y = 0
                self.x = random.randint(0, self.screen.width)
