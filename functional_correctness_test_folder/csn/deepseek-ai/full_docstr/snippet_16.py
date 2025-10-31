
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
        self._screen = screen
        self._x = x
        self._chars = []
        self._speed = random.uniform(0.1, 0.5)
        self._length = random.randint(5, 15)
        self._current_pos = 0
        self._reseed_counter = 0

    def _maybe_reseed(self, normal: bool):
        '''
        Randomly create a new column once this one is finished.
        '''
        if normal:
            if random.random() < 0.3:
                self._chars = []
                self._current_pos = 0
                self._length = random.randint(5, 15)
                self._speed = random.uniform(0.1, 0.5)
        else:
            if self._reseed_counter >= 3:
                self._chars = []
                self._current_pos = 0
                self._length = random.randint(5, 15)
                self._speed = random.uniform(0.1, 0.5)
                self._reseed_counter = 0
            else:
                self._reseed_counter += 1

    def update(self, reseed: bool):
        '''
        Update that trail!
        :param reseed: Whether we are in the normal reseed cycle or not.
        '''
        if not self._chars or self._current_pos >= self._length:
            self._maybe_reseed(reseed)
            return

        self._current_pos += self._speed
        if self._current_pos >= self._length:
            self._maybe_reseed(reseed)
