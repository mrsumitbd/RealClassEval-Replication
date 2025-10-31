
import random
from turtle import Screen


class _Trail:

    def __init__(self, screen: Screen, x: int):
        self.screen = screen
        self.x = x
        self.height = int(screen.window_height())
        self.y = random.randint(-self.height // 2, self.height // 2)
        self.length = random.randint(5, 20)
        self.speed = random.randint(2, 10)
        self.counter = 0

    def _maybe_reseed(self, normal: bool):
        if normal:
            self.y = random.randint(-self.height // 2, self.height // 2)
            self.length = random.randint(5, 20)
            self.speed = random.randint(2, 10)
        else:
            self.y = -self.height // 2
            self.length = random.randint(5, 20)
            self.speed = random.randint(2, 10)
        self.counter = 0

    def update(self, reseed: bool):
        if reseed or self.y > self.height // 2:
            self._maybe_reseed(normal=not reseed)
        else:
            self.y += self.speed
            self.counter += 1
