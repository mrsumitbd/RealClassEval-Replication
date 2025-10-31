
import random


class _Star:

    def __init__(self, screen: 'Screen', pattern: str):
        self.screen = screen
        self.pattern = pattern
        self.current_pattern_index = 0
        self.x, self.y = self._respawn()

    def _respawn(self):
        max_x, max_y = self.screen.getmaxyx()
        while True:
            x = random.randint(0, max_x - 1)
            y = random.randint(0, max_y - 1)
            if self.screen.instr(y, x) == b' ':
                return x, y

    def update(self):
        self.screen.addch(
            self.y, self.x, self.pattern[self.current_pattern_index])
        self.current_pattern_index = (
            self.current_pattern_index + 1) % len(self.pattern)
        self.x, self.y = self._respawn()
