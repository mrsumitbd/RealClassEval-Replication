import random


class _Star:

    def __init__(self, screen, pattern: str):
        '''
        :param screen: The Screen being used for the Scene.
        :param pattern: The pattern to loop through
        '''
        self._screen = screen
        self._pattern = pattern or "*"
        self._i = random.randrange(len(self._pattern))
        self._x = None
        self._y = None
        self._last_drawn = None
        self._respawn()

    def _get_char_at(self, x, y):
        try:
            cell = self._screen.get_from(x, y)
        except Exception:
            return " "
        # Try to handle both tuple and object with .char
        if cell is None:
            return " "
        ch = None
        if hasattr(cell, "char"):
            ch = cell.char
        else:
            try:
                ch = cell[0]
            except Exception:
                ch = str(cell)
        if ch is None:
            return " "
        # Normalize to a single character if possible
        if isinstance(ch, (list, tuple)) and ch:
            ch = ch[0]
        return ch if isinstance(ch, str) and len(ch) > 0 else " "

    def _is_empty(self, x, y):
        ch = self._get_char_at(x, y)
        return ch == " " or ch == "\x00"

    def _respawn(self):
        '''
        Pick a random location for the star making sure it does
        not overwrite an existing piece of text.
        '''
        width = getattr(self._screen, "width", None)
        height = getattr(self._screen, "height", None)
        if not isinstance(width, int) or not isinstance(height, int) or width <= 0 or height <= 0:
            # Fallback if screen doesn't expose width/height
            width = 80
            height = 24

        for _ in range(200):
            x = random.randrange(0, max(1, width))
            y = random.randrange(0, max(1, height))
            if self._is_empty(x, y):
                self._x, self._y = x, y
                self._last_drawn = None
                return

        # If we couldn't find an empty spot, place it anywhere and allow overwrite
        self._x = random.randrange(0, max(1, width))
        self._y = random.randrange(0, max(1, height))
        self._last_drawn = None

    def update(self):
        if self._x is None or self._y is None:
            self._respawn()

        # Advance pattern
        self._i = (self._i + 1) % len(self._pattern)
        ch = self._pattern[self._i]

        # If target cell has been occupied by something else, respawn
        current = self._get_char_at(self._x, self._y)
        if current not in (" ", "\x00") and current != self._last_drawn:
            self._respawn()

        # Draw at current location
        try:
            self._screen.print_at(ch, self._x, self._y)
            self._last_drawn = ch
        except Exception:
            # If draw fails, try to respawn next time
            self._last_drawn = None
            self._x = None
            self._y = None
