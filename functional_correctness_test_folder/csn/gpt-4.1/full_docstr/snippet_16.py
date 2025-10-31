
import random
import string


class _Trail:
    '''
    Track a single trail for a falling character effect (a la Matrix).
    '''

    def __init__(self, screen, x: int):
        '''
        :param screen: The Screen being used for the Scene.
        :param x: The column (y coordinate) for this trail to use.
        '''
        self._screen = screen
        self._x = x
        self._height = screen.height
        self._reset()

    def _reset(self):
        self._length = random.randint(5, self._height // 2)
        self._y = random.randint(-self._height, 0)
        self._chars = [random.choice(
            string.ascii_letters + string.digits) for _ in range(self._length)]

    def _maybe_reseed(self, normal: bool):
        '''
        Randomly create a new column once this one is finished.
        '''
        if self._y - self._length > self._height:
            if normal:
                if random.random() < 0.5:
                    self._reset()
            else:
                self._reset()

    def update(self, reseed: bool):
        '''
        Update that trail!
        :param reseed: Whether we are in the normal reseed cycle or not.
        '''
        # Erase previous trail
        for i in range(self._length):
            y = self._y - i
            if 0 <= y < self._height:
                self._screen.print_at(' ', self._x, y)
        # Move trail down
        self._y += 1
        # Draw new trail
        for i in range(self._length):
            y = self._y - i
            if 0 <= y < self._height:
                char = self._chars[i]
                if i == 0:
                    # Head of the trail (bright)
                    self._screen.print_at(char, self._x, y, colour=7)
                else:
                    # Body of the trail (dim)
                    self._screen.print_at(char, self._x, y, colour=2)
        self._maybe_reseed(reseed)
