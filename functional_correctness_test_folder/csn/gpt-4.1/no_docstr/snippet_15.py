
import random


class _Star:

    def __init__(self, screen, pattern: str):
        self.screen = screen
        self.pattern = pattern
        self._respawn()

    def _respawn(self):
        self.x = random.randint(0, self.screen.width - 1)
        self.y = 0

    def update(self):
        # Erase previous position
        if 0 <= self.y < self.screen.height and 0 <= self.x < self.screen.width:
            self.screen.put(self.x, self.y, ' ')
        self.y += 1
        if self.y >= self.screen.height:
            self._respawn()
        # Draw at new position
        if 0 <= self.y < self.screen.height and 0 <= self.x < self.screen.width:
            self.screen.put(self.x, self.y, self.pattern)
