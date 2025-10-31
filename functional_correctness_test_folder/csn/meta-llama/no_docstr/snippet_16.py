
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from screen import Screen  # Assuming Screen is defined in screen.py


class _Trail:

    def __init__(self, screen: 'Screen', x: int):
        self.screen = screen
        self.x = x
        self.y = random.randint(0, screen.height - 1)
        self.length = random.randint(1, screen.height // 2)
        self.normal = True

    def _maybe_reseed(self, normal: bool):
        if self.normal != normal:
            self.y = random.randint(0, self.screen.height - 1)
            self.length = random.randint(1, self.screen.height // 2)
            self.normal = normal

    def update(self, reseed: bool):
        if reseed:
            self._maybe_reseed(True)
        else:
            self.y += 1
            if self.y >= self.screen.height:
                self.y = 0
                self._maybe_reseed(False)
        self.screen.draw_trail(self.x, self.y, self.length)
