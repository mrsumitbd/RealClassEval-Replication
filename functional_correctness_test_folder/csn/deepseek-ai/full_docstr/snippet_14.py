
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from screen import Screen


class _Flake:
    '''
    Track a single snow flake.
    '''

    def __init__(self, screen: 'Screen'):
        '''
        :param screen: The Screen being used for the Scene.
        '''
        self.screen = screen
        self._reseed()

    def _reseed(self):
        '''
        Randomly create a new snowflake once this one is finished.
        '''
        self.x = random.randint(0, self.screen.width - 1)
        self.y = random.randint(-10, -1)
        self.speed = random.uniform(0.5, 2.0)

    def update(self, reseed: bool):
        '''
        Update that snowflake!
        :param reseed: Whether we are in the normal reseed cycle or not.
        '''
        self.y += self.speed
        if self.y >= self.screen.height or (reseed and random.random() < 0.01):
            self._reseed()
