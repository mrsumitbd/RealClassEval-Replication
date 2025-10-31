from random import randint, random, choice
from asciimatics.screen import Screen

class _Star:
    """
    Simple class to represent a single star for the Stars special effect.
    """

    def __init__(self, screen: Screen, pattern: str):
        """
        :param screen: The Screen being used for the Scene.
        :param pattern: The pattern to loop through
        """
        self._screen = screen
        self._star_chars = pattern
        self._cycle = 0
        self._old_char = ''
        self._respawn()

    def _respawn(self):
        """
        Pick a random location for the star making sure it does
        not overwrite an existing piece of text.
        """
        self._cycle = randint(0, len(self._star_chars))
        height, width = self._screen.dimensions
        while True:
            self._x = randint(0, width - 1)
            self._y = self._screen.start_line + randint(0, height - 1)
            c = self._screen.get_from(self._x, self._y)
            if c is not None and c[0] == 32:
                break
        self._old_char = ' '

    def update(self):
        """
        Draw the star.
        """
        if not self._screen.is_visible(self._x, self._y):
            self._respawn()
        c = self._screen.get_from(self._x, self._y)
        if c is not None and c[0] not in (ord(self._old_char), 32):
            self._respawn()
        self._cycle += 1
        if self._cycle >= len(self._star_chars):
            self._cycle = 0
        new_char = self._star_chars[self._cycle]
        if new_char == self._old_char:
            return
        self._screen.print_at(new_char, self._x, self._y)
        self._old_char = new_char