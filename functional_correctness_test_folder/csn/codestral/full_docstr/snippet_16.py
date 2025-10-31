
import random


class _Trail:
    '''
    Track a single trail  for a falling character effect (a la Matrix).
    '''

    def __init__(self, screen: Screen, x: int):
        '''
        :param screen: The Screen being used for the Scene.
        :param x: The column (y coordinate) for this trail to use.
        '''
        self.screen = screen
        self.x = x
        self.y = 0
        self.length = random.randint(5, 20)
        self.speed = random.uniform(0.1, 0.5)
        self.char = chr(random.randint(33, 126))
        self.active = True

    def _maybe_reseed(self, normal: bool):
        '''
        Randomly create a new column once this one is finished.
        '''
        if not self.active and (normal or random.random() < 0.1):
            self.y = 0
            self.length = random.randint(5, 20)
            self.speed = random.uniform(0.1, 0.5)
            self.char = chr(random.randint(33, 126))
            self.active = True

    def update(self, reseed: bool):
        '''
        Update that trail!
        :param reseed: Whether we are in the normal reseed cycle or not.
        '''
        if self.active:
            self.y += self.speed
            if self.y >= self.length:
                self.active = False
            else:
                self.screen.print_at(self.char, self.x, int(self.y))
        else:
            self._maybe_reseed(reseed)
