import random
from typing import Optional


class _Star:

    def __init__(self, screen, pattern: str):
        self._screen = screen
        self._pattern = pattern or "*"
        self._width = getattr(screen, "width", 0)
        self._height = getattr(screen, "height", 0)
        self._prev_x: Optional[int] = None
        self._prev_y: Optional[int] = None
        self._x: float = 0.0
        self._y: float = 0.0
        self._vy: float = 0.0
        self._char: str = "*"
        self._colour: int = 7
        self._respawn()

    def _respawn(self):
        if self._width <= 0 or self._height <= 0:
            self._x = 0
            self._y = 0
            self._vy = 0.0
            self._char = "*"
            self._colour = 7
            return
        self._x = random.randint(0, self._width - 1)
        self._y = -1.0
        self._vy = random.uniform(0.2, 1.5)
        self._char = random.choice(self._pattern)
        max_colour = getattr(self._screen, "colours", 8) - 1
        max_colour = max(1, max_colour)
        self._colour = random.randint(1, max_colour)

    def update(self):
        # Erase previous position
        if self._prev_x is not None and self._prev_y is not None:
            if 0 <= self._prev_x < self._width and 0 <= self._prev_y < self._height:
                try:
                    self._screen.print_at(" ", self._prev_x, self._prev_y)
                except Exception:
                    pass

        self._y += self._vy

        if self._y >= self._height:
            self._prev_x = None
            self._prev_y = None
            self._respawn()
            return

        ix = int(self._x)
        iy = int(self._y)

        if 0 <= ix < self._width and 0 <= iy < self._height:
            try:
                self._screen.print_at(self._char, ix, iy, self._colour)
            except Exception:
                pass

        self._prev_x = ix
        self._prev_y = iy
