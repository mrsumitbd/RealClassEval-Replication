
import random


class _Star:

    def __init__(self, screen: Screen, pattern: str):
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
        max_y, max_x = self._screen.getmaxyx()
        while True:
            self._x = random.randint(0, max_x - 1)
            self._y = random.randint(0, max_y - 1)
            # Check if the position is empty (assuming getyx returns the current character)
            if self._screen.inch(self._y, self._x) == ord(' '):
                break

    def update(self):
        char = self._pattern[self._pattern_index]
        self._screen.addch(self._y, self._x, char)
        self._pattern_index = (self._pattern_index + 1) % len(self._pattern)
