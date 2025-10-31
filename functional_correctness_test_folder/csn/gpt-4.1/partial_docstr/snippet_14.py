
import random


class _Flake:
    '''
    Track a single snow flake.
    '''

    def __init__(self, screen):
        self.screen = screen
        self._reseed()

    def _reseed(self):
        self.x = random.randint(0, self.screen.width - 1)
        self.y = 0
        self.char = random.choice(['*', '+', '.', 'o'])
        self.speed = random.randint(1, 2)

    def update(self, reseed: bool):
        '''
        Update that snowflake!
        :param reseed: Whether we are in the normal reseed cycle or not.
        '''
        self.y += self.speed
        if self.y >= self.screen.height or reseed:
            self._reseed()
