
import random
from typing import List, Optional


class _Trail:
    '''
    Track a single trail for a falling character effect (a la Matrix).
    '''

    def __init__(self, screen: Screen, x: int):
        self.screen = screen
        self.x = x
        self.chars: List[str] = []
        self.positions: List[int] = []
        self.speeds: List[int] = []
        self._reseed_count = 0
        self._reseed_threshold = random.randint(5, 15)

    def _maybe_reseed(self, normal: bool):
        if normal:
            self._reseed_count += 1
            if self._reseed_count >= self._reseed_threshold:
                self._reseed_count = 0
                self._reseed_threshold = random.randint(5, 15)
                return True
        else:
            if random.random() < 0.1:
                return True
        return False

    def update(self, reseed: bool):
        '''
        Update that trail!
        :param reseed: Whether we are in the normal reseed cycle or not.
        '''
        if self._maybe_reseed(reseed):
            char = chr(random.randint(33, 126))
            self.chars.append(char)
            self.positions.append(0)
            self.speeds.append(random.randint(1, 3))

        for i in range(len(self.positions)):
            self.positions[i] += self.speeds[i]

        # Remove characters that have fallen off the screen
        height = self.screen.getmaxyx()[0]
        to_remove = [i for i, pos in enumerate(
            self.positions) if pos >= height]
        for i in sorted(to_remove, reverse=True):
            del self.chars[i]
            del self.positions[i]
            del self.speeds[i]
