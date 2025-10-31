import random
import string
from typing import List
from asciimatics.screen import Screen


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
        self._x = max(0, min(x, self._screen.width - 1))
        self._charset = string.ascii_letters + string.digits + string.punctuation
        self._length = random.randint(
            max(5, self._screen.height // 6), max(8, self._screen.height // 3))
        self._y = -random.randint(0, self._screen.height)  # start above screen
        self._chars: List[str] = []
        self._active = True

    def _maybe_reseed(self, normal: bool):
        '''
        Randomly create a new column once this one is finished.
        '''
        finished = self._y - self._length > self._screen.height
        if not finished:
            return

        if normal:
            # In normal cycle, only sometimes reseed to avoid constant density.
            if random.random() < 0.02:
                self._length = random.randint(
                    max(5, self._screen.height // 6), max(8, self._screen.height // 3))
                self._y = -random.randint(0, self._screen.height)
                self._chars.clear()
                self._active = True
            else:
                self._active = False
        else:
            # Forced cycle: always reseed.
            self._length = random.randint(
                max(5, self._screen.height // 6), max(8, self._screen.height // 3))
            self._y = -random.randint(0, self._screen.height)
            self._chars.clear()
            self._active = True

    def update(self, reseed: bool):
        '''
        Update that trail!
        :param reseed: Whether we are in the normal reseed cycle or not.
        '''
        if not self._active:
            # If not currently active, try to reseed and return.
            self._maybe_reseed(reseed)
            return

        # Append a new head character.
        head_char = random.choice(self._charset)
        self._chars.insert(0, head_char)
        if len(self._chars) > self._length:
            self._chars.pop()

        # Clear the cell that trails beyond the bottom.
        tail_y = int(self._y - self._length)
        if 0 <= tail_y < self._screen.height:
            self._screen.print_at(" ", self._x, tail_y)

        # Draw from head to tail with diminishing intensity.
        for i, ch in enumerate(self._chars):
            y = int(self._y - i)
            if 0 <= y < self._screen.height:
                if i == 0:
                    # Head - bright white
                    self._screen.print_at(ch, self._x, y,
                                          colour=Screen.COLOUR_WHITE,
                                          attr=Screen.A_BOLD)
                elif i < min(3, self._length):
                    # Near head - bold green
                    self._screen.print_at(ch, self._x, y,
                                          colour=Screen.COLOUR_GREEN,
                                          attr=Screen.A_BOLD)
                else:
                    # Tail - normal green
                    self._screen.print_at(ch, self._x, y,
                                          colour=Screen.COLOUR_GREEN,
                                          attr=Screen.A_NORMAL)

        # Move trail down.
        self._y += 1

        # Maybe reseed if finished.
        self._maybe_reseed(reseed)
