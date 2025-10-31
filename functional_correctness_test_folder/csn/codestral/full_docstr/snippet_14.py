
import random


class _Flake:
    '''
    Track a single snow flake.
    '''

    def __init__(self, screen: Screen):
        '''
        :param screen: The Screen being used for the Scene.
        '''
        self.screen = screen
        self.x = random.randint(0, screen.width)
        self.y = random.randint(-screen.height, 0)
        self.speed = random.uniform(0.5, 2.0)
        self.size = random.randint(1, 3)

    def _reseed(self):
        '''
        Randomly create a new snowflake once this one is finished.
        '''
        self.x = random.randint(0, self.screen.width)
        self.y = random.randint(-self.screen.height, 0)
        self.speed = random.uniform(0.5, 2.0)
        self.size = random.randint(1, 3)

    def update(self, reseed: bool):
        '''
        Update that snowflake!
        :param reseed: Whether we are in the normal reseed cycle or not.
        '''
        self.y += self.speed
        if self.y > self.screen.height or reseed:
            self._reseed()
