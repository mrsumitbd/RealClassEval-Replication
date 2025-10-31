from random import randint, random, choice
from asciimatics.screen import Screen

class _Trail:
    """
    Track a single trail  for a falling character effect (a la Matrix).
    """

    def __init__(self, screen: Screen, x: int):
        """
        :param screen: The Screen being used for the Scene.
        :param x: The column (y coordinate) for this trail to use.
        """
        self._screen = screen
        self._x = x
        self._y = 0
        self._life = 0
        self._rate = 0
        self._clear = True
        self._maybe_reseed(True)

    def _maybe_reseed(self, normal: bool):
        """
        Randomly create a new column once this one is finished.
        """
        self._y += self._rate
        self._life -= 1
        if self._life <= 0:
            self._clear = not self._clear if normal else True
            self._rate = randint(1, 2)
            if self._clear:
                self._y = 0
                self._life = self._screen.height // self._rate
            else:
                self._y = randint(0, self._screen.height // 2) - self._screen.height // 4
                self._life = randint(1, self._screen.height - self._y) // self._rate

    def update(self, reseed: bool):
        """
        Update that trail!

        :param reseed: Whether we are in the normal reseed cycle or not.
        """
        if self._clear:
            for i in range(0, 3):
                self._screen.print_at(' ', self._x, self._screen.start_line + self._y + i)
            self._maybe_reseed(reseed)
        else:
            for i in range(0, 3):
                self._screen.print_at(chr(randint(32, 126)), self._x, self._screen.start_line + self._y + i, Screen.COLOUR_GREEN)
            for i in range(4, 6):
                self._screen.print_at(chr(randint(32, 126)), self._x, self._screen.start_line + self._y + i, Screen.COLOUR_GREEN, Screen.A_BOLD)
            self._maybe_reseed(reseed)