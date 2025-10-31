
import random


class _Flake:
    '''
    Track a single snow flake.
    '''

    def __init__(self, screen):
        '''
        :param screen: The Screen being used for the Scene.
        '''
        self._screen = screen
        self._reseed()

    def _reseed(self):
        '''
        Randomly create a new snowflake once this one is finished.
        '''
        self._x = random.randint(0, self._screen.width - 1)
        self._y = 0
        self._char = random.choice(['*', '.', '+', 'o'])
        self._speed = random.choice([1, 1, 1, 2])  # More likely to be 1
        self._counter = 0

    def update(self, reseed: bool):
        '''
        Update that snowflake!
        :param reseed: Whether we are in the normal reseed cycle or not.
        '''
        # Erase previous position if needed
        if 0 <= self._y < self._screen.height:
            self._screen.print_at(' ', self._x, self._y)

        self._counter += 1
        if self._counter >= self._speed:
            self._y += 1
            self._counter = 0

        if self._y >= self._screen.height:
            if reseed:
                self._reseed()
            else:
                self._y = self._screen.height - 1

        # Draw at new position if on screen
        if 0 <= self._y < self._screen.height:
            self._screen.print_at(self._char, self._x, self._y)
