
import random


class _Star:

    def __init__(self, screen: Screen, pattern: str):
        self.screen = screen
        self.pattern = pattern
        self.x = random.randint(0, screen.width - 1)
        self.y = random.randint(0, screen.height - 1)
        self.speed = random.uniform(0.1, 1.0)

    def _respawn(self):
        self.x = random.randint(0, self.screen.width - 1)
        self.y = 0
        self.speed = random.uniform(0.1, 1.0)

    def update(self):
        self.y += self.speed
        if self.y >= self.screen.height:
            self._respawn()
        self.screen.draw(self.pattern, self.x, self.y)
