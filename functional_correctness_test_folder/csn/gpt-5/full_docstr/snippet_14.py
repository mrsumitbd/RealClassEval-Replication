import random
from typing import Optional


class _Flake:
    '''
    Track a single snow flake.
    '''

    def __init__(self, screen):
        '''
        :param screen: The Screen being used for the Scene.
        '''
        self._screen = screen
        self._x: int = 0
        self._y: int = 0
        self._prev: Optional[tuple[int, int]] = None
        self._delay: int = 1
        self._counter: int = 0
        self._char: str = "*"
        self._colour = getattr(screen, "COLOUR_WHITE", None)
        self._attr = getattr(screen, "A_BOLD", 0)
        self._bg = getattr(screen, "COLOUR_BLACK", None)
        self._dead: bool = False
        self._drift_prob: float = 0.3
        self._spread_init: bool = True
        self._reseed()

    def _screen_size(self):
        if hasattr(self._screen, "width") and hasattr(self._screen, "height"):
            return self._screen.width, self._screen.height
        if hasattr(self._screen, "dimensions"):
            w, h = self._screen.dimensions
            return w, h
        # Fallback to something safe
        return 80, 24

    def _reseed(self):
        '''
        Randomly create a new snowflake once this one is finished.
        '''
        width, height = self._screen_size()
        if width <= 0 or height <= 0:
            self._dead = True
            return

        # Generate a new flake
        self._x = random.randrange(0, max(1, width))
        # First seed: random y to populate the sky. Subsequent reseeds: start at the top.
        if self._spread_init:
            self._y = random.randrange(0, max(1, height))
            self._spread_init = False
        else:
            self._y = 0

        self._prev = None
        self._counter = 0
        # Delay controls falling speed (higher = slower)
        self._delay = random.randint(1, 3)
        # Choose a glyph with a rough correlation to "weight"
        glyphs = [".", ".", ".", "*", "+"]
        self._char = random.choice(glyphs)
        # Randomize attribute slightly
        self._attr = getattr(self._screen, "A_BOLD", 0) if random.random(
        ) < 0.5 else getattr(self._screen, "A_NORMAL", 0)
        self._dead = False

    def update(self, reseed: bool):
        '''
        Update that snowflake!
        :param reseed: Whether we are in the normal reseed cycle or not.
        '''
        if self._dead:
            if reseed:
                self._reseed()
            return

        width, height = self._screen_size()
        if width <= 0 or height <= 0:
            self._dead = True
            return

        # Erase previous position
        if self._prev is not None:
            px, py = self._prev
            if 0 <= px < width and 0 <= py < height:
                try:
                    # print space to erase
                    self._screen.print_at(" ", px, py, self._colour, getattr(
                        self._screen, "A_NORMAL", 0), self._bg)
                except Exception:
                    pass

        # Move according to delay
        self._counter += 1
        if self._counter >= self._delay:
            self._counter = 0
            # Vertical fall
            self._y += 1
            # Random horizontal drift
            if random.random() < self._drift_prob:
                self._x += random.choice((-1, 0, 1))
                if self._x < 0:
                    self._x = 0
                elif self._x >= width:
                    self._x = width - 1

        # Out of screen bottom
        if self._y >= height:
            if reseed:
                self._reseed()
            else:
                self._dead = True
            return

        # Draw at new position
        if 0 <= self._x < width and 0 <= self._y < height and not self._dead:
            try:
                self._screen.print_at(
                    self._char, self._x, self._y, self._colour, self._attr, self._bg)
            except Exception:
                # Be resilient to differing Screen implementations
                try:
                    self._screen.print_at(self._char, self._x, self._y)
                except Exception:
                    pass

        self._prev = (self._x, self._y)
