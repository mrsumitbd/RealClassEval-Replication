import random
from typing import Optional
try:
    from asciimatics.screen import Screen
except Exception:
    # Fallback type hint if asciimatics isn't available at runtime
    Screen = object  # type: ignore


class _Star:
    '''
    Simple class to represent a single star for the Stars special effect.
    '''

    def __init__(self, screen: Screen, pattern: str):
        '''
        :param screen: The Screen being used for the Scene.
        :param pattern: The pattern to loop through
        '''
        self._screen = screen
        self._pattern = pattern or "*"
        self._index = 0
        self._x: Optional[int] = None
        self._y: Optional[int] = None
        self._respawn()

    def _empty_at(self, x: int, y: int) -> bool:
        try:
            cell = self._screen.get_from(x, y)
            if cell is None:
                return False
            ch = cell[0]
            return ch == " "
        except Exception:
            # If screen can't provide cell info, assume not empty to be safe.
            return False

    def _respawn(self):
        '''
        Pick a random location for the star making sure it does
        not overwrite an existing piece of text.
        '''
        width = getattr(self._screen, "width", 0)
        height = getattr(self._screen, "height", 0)
        if width <= 0 or height <= 0:
            self._x, self._y = 0, 0
            return

        for _ in range(200):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            if self._empty_at(x, y):
                self._x, self._y = x, y
                return

        # Fallback: pick a location even if occupied to avoid infinite loops
        self._x = 0 if self._x is None else max(0, min(self._x, width - 1))
        self._y = 0 if self._y is None else max(0, min(self._y, height - 1))

    def update(self):
        '''
        Draw the star.
        '''
        if self._x is None or self._y is None:
            self._respawn()

        # Move if our current location is now occupied
        if not self._empty_at(self._x, self._y):
            self._respawn()

        ch = self._pattern[self._index % len(self._pattern)]
        try:
            self._screen.print_at(ch, self._x, self._y)
        except TypeError:
            # Some Screen implementations may require full parameters; try with defaults
            self._screen.print_at(ch, self._x, self._y, 7, 0, 0, False)

        self._index = (self._index + 1) % len(self._pattern)
