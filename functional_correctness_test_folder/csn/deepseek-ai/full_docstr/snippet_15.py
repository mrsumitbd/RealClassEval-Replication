
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from terminal_engine import Screen


class _Star:
    '''
    Simple class to represent a single star for the Stars special effect.
    '''

    def __init__(self, screen: 'Screen', pattern: str):
        '''
        :param screen: The Screen being used for the Scene.
        :param pattern: The pattern to loop through
        '''
        self._screen = screen
        self._pattern = pattern
        self._pattern_index = 0
        self._x = 0
        self._y = 0
        self._respawn()

    def _respawn(self):
        '''
        Pick a random location for the star making sure it does
        not overwrite an existing piece of text.
        '''
        width, height = self._screen.size
        while True:
            self._x = random.randint(0, width - 1)
            self._y = random.randint(0, height - 1)
            if self._screen.get(self._x, self._y) == ' ':
                break

    def update(self):
        '''
        Draw the star.
        '''
        char = self._pattern[self._pattern_index]
        self._screen.draw(self._x, self._y, char)
        self._pattern_index = (self._pattern_index + 1) % len(self._pattern)
