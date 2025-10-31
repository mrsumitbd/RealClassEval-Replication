
import random


class _Star:

    def __init__(self, screen: 'Screen', pattern: str):
        self.screen = screen
        self.pattern = pattern
        self.position = (0, 0)
        self._respawn()

    def _respawn(self):
        max_x, max_y = self.screen.get_dimensions()
        while True:
            x = random.randint(0, max_x - 1)
            y = random.randint(0, max_y - 1)
            if self.screen.get_char(x, y) == ' ':
                self.position = (x, y)
                break

    def update(self):
        x, y = self.position
        current_char = self.screen.get_char(x, y)
        if current_char == self.pattern[-1]:
            self.screen.set_char(x, y, ' ')
            self._respawn()
        else:
            index = self.pattern.index(
                current_char) if current_char in self.pattern else -1
            next_char = self.pattern[index + 1] if index + \
                1 < len(self.pattern) else self.pattern[0]
            self.screen.set_char(x, y, next_char)
