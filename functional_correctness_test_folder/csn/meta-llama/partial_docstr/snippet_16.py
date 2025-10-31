
import random


class _Trail:
    '''
    Track a single trail  for a falling character effect (a la Matrix).
    '''

    def __init__(self, screen: 'Screen', x: int):
        self.screen = screen
        self.x = x
        self.y = random.randint(-screen.height, 0)
        self.length = random.randint(5, 15)
        self.chars = [random.choice('0123456789ABCDEF')
                      for _ in range(self.length)]

    def _maybe_reseed(self, normal: bool):
        if self.y > self.screen.height or (normal and random.random() < 0.1):
            self.y = random.randint(-self.screen.height, 0)
            self.length = random.randint(5, 15)
            self.chars = [random.choice('0123456789ABCDEF')
                          for _ in range(self.length)]

    def update(self, reseed: bool):
        '''
        Update that trail!
        :param reseed: Whether we are in the normal reseed cycle or not.
        '''
        self._maybe_reseed(reseed)
        self.y += 1
        self.screen.print_at(
            self.chars[0], self.x, self.y - self.length, colour=(0, 255, 0))
        for i in range(1, self.length):
            if self.y - i >= 0 and self.y - i < self.screen.height:
                self.screen.print_at(
                    self.chars[i], self.x, self.y - i, colour=(0, int(255 * (1 - i / self.length)), 0))
