
import random


class _Flake:
    '''
    Track a single snow flake.
    '''

    def __init__(self, screen: 'Screen'):
        self.screen = screen
        self._reseed()

    def _reseed(self):
        self.x = random.randint(0, self.screen.width)
        self.y = random.randint(-50, -10)
        self.size = random.randint(2, 5)
        self.speed = random.uniform(1.0, 3.0)

    def update(self, reseed: bool):
        '''
        Update that snowflake!
        :param reseed: Whether we are in the normal reseed cycle or not.
        '''
        self.y += self.speed
        if self.y > self.screen.height or reseed:
            self._reseed()
