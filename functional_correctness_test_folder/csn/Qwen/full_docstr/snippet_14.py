
import random


class _Flake:
    '''
    Track a single snow flake.
    '''

    def __init__(self, screen: 'Screen'):
        '''
        :param screen: The Screen being used for the Scene.
        '''
        self.screen = screen
        self.x = random.randint(0, screen.width)
        self.y = random.randint(-50, -10)
        self.size = random.randint(2, 5)
        self.speed = random.uniform(1.0, 3.0)

    def _reseed(self):
        '''
        Randomly create a new snowflake once this one is finished.
        '''
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
