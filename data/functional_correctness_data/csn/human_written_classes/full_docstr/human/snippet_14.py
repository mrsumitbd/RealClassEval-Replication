from random import randint, random, choice
from asciimatics.screen import Screen

class _Flake:
    """
    Track a single snow flake.
    """
    _snow_chars = '.+*'
    _drift_chars = ' ,;#@'

    def __init__(self, screen: Screen):
        """
        :param screen: The Screen being used for the Scene.
        """
        self._screen = screen
        self._x = 0
        self._y = 0
        self._rate = 0
        self._char = ''
        self._reseed()

    def _reseed(self):
        """
        Randomly create a new snowflake once this one is finished.
        """
        self._char = choice(self._snow_chars)
        self._rate = randint(1, 3)
        self._x = randint(0, self._screen.width - 1)
        self._y = self._screen.start_line + randint(0, self._rate)

    def update(self, reseed: bool):
        """
        Update that snowflake!

        :param reseed: Whether we are in the normal reseed cycle or not.
        """
        self._screen.print_at(' ', self._x, self._y)
        cell = None
        for _ in range(self._rate):
            self._y += 1
            cell = self._screen.get_from(self._x, self._y)
            if cell is None or cell[0] != 32:
                break
        if (cell is not None and cell[0] in [ord(x) for x in self._snow_chars + ' ']) and self._y < self._screen.start_line + self._screen.height:
            self._screen.print_at(self._char, self._x, self._y)
        else:
            self._y = min(self._y, self._screen.start_line + self._screen.height)
            drift_index = -1
            if cell:
                drift_index = self._drift_chars.find(chr(cell[0]))
            if 0 <= drift_index < len(self._drift_chars) - 1:
                drift_char = self._drift_chars[drift_index + 1]
                self._screen.print_at(drift_char, self._x, self._y)
            else:
                self._screen.print_at(',', self._x, self._y - 1)
            if reseed:
                self._reseed()