import random
from typing import Optional


class _Flake:
    '''
    Track a single snow flake.
    '''

    def __init__(self, screen):
        self._screen = screen
        self._width = getattr(screen, "width", None)
        self._height = getattr(screen, "height", None)
        if self._width is None or self._height is None:
            # Try curses-like api
            try:
                self._height, self._width = screen.getmaxyx()
            except Exception:
                raise ValueError(
                    "Screen must provide width/height or getmaxyx()")

        self._x: float = 0.0
        self._y: float = 0.0
        self._prev_x: Optional[int] = None
        self._prev_y: Optional[int] = None
        self._dx: float = 0.0
        self._speed: float = 0.0
        self._glyph: str = "*"
        self._reseed()

    def _reseed(self):
        self._x = float(random.randrange(0, max(1, self._width)))
        # Start slightly above the top to stagger arrival
        self._y = float(-random.randrange(0, max(1, self._height // 4 + 1)))
        self._dx = random.choice([-0.5, -0.25, 0.0, 0.25, 0.5])
        # Speed biases toward slower flakes for better density
        self._speed = random.choice([0.25, 0.25, 0.5, 0.5, 0.75, 1.0])
        # Choose glyph by "size"/speed
        if self._speed <= 0.25:
            self._glyph = "."
        elif self._speed <= 0.5:
            self._glyph = "·"
        elif self._speed <= 0.75:
            self._glyph = "o"
        else:
            self._glyph = "*"
        self._prev_x = None
        self._prev_y = None

    def update(self, reseed: bool):
        '''
        Update that snowflake!
        :param reseed: Whether we are in the normal reseed cycle or not.
        '''
        # Erase previous position
        if self._prev_x is not None and self._prev_y is not None:
            if 0 <= self._prev_x < self._width and 0 <= self._prev_y < self._height:
                try:
                    self._screen.print_at(" ", self._prev_x, self._prev_y)
                except Exception:
                    pass

        # Occasionally vary horizontal drift
        if random.random() < 0.1:
            self._dx += random.choice([-0.25, 0.0, 0.25])
            self._dx = max(-0.75, min(0.75, self._dx))

        # Apply movement
        self._x += self._dx
        self._y += self._speed

        # Handle edges
        out_of_bounds = (
            self._y >= self._height or
            self._x < 0 or
            self._x >= self._width
        )

        if out_of_bounds:
            if reseed:
                self._reseed()
            else:
                # Clamp within screen without reseeding
                self._x = max(0.0, min(float(self._width - 1), self._x))
                self._y = max(0.0, min(float(self._height - 1), self._y))

        # Draw current position
        ix = int(self._x)
        iy = int(self._y)
        if 0 <= ix < self._width and 0 <= iy < self._height:
            try:
                self._screen.print_at(self._glyph, ix, iy)
            except Exception:
                pass

        # Remember for erase next frame
        self._prev_x = ix
        self._prev_y = iy
