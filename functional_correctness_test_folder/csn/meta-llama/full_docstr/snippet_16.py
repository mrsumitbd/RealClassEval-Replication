
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
        self._screen = screen
        self._x = x
        self._y = 0
        self._length = random.randint(5, 15)
        self._chars = [random.choice(
            'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(self._length)]
        self._done = False

    def _maybe_reseed(self, normal: bool):
        '''
        Randomly create a new column once this one is finished.
        '''
        if self._done and (normal or random.random() < 0.1):
            self._y = 0
            self._length = random.randint(5, 15)
            self._chars = [random.choice(
                'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(self._length)]
            self._done = False

    def update(self, reseed: bool):
        '''
        Update that trail!
        :param reseed: Whether we are in the normal reseed cycle or not.
        '''
        self._screen.move(self._x, self._y, ' ')
        if not self._done:
            self._screen.print_at(
                self._chars[self._y % self._length], self._x, self._y)
            self._y += 1
            if self._y >= self._screen.height:
                self._done = True
        self._maybe_reseed(reseed)
