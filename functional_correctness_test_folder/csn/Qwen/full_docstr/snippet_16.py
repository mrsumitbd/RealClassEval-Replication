
import random


class _Trail:
    '''
    Track a single trail  for a falling character effect (a la Matrix).
    '''

    def __init__(self, screen: 'Screen', x: int):
        '''
        :param screen: The Screen being used for the Scene.
        :param x: The column (y coordinate) for this trail to use.
        '''
        self.screen = screen
        self.x = x
        self.length = 0
        self.max_length = random.randint(5, 20)
        self.y = 0

    def _maybe_reseed(self, normal: bool):
        '''
        Randomly create a new column once this one is finished.
        '''
        if self.y >= self.screen.height or self.length >= self.max_length:
            if normal or random.random() < 0.05:
                self.y = 0
                self.length = 0
                self.max_length = random.randint(5, 20)
                self.x = random.randint(0, self.screen.width - 1)

    def update(self, reseed: bool):
        '''
        Update that trail!
        :param reseed: Whether we are in the normal reseed cycle or not.
        '''
        if self.y < self.screen.height and self.length < self.max_length:
            self.screen.set_char(self.y, self.x, '*')
            self.y += 1
            self.length += 1
        self._maybe_reseed(reseed)
