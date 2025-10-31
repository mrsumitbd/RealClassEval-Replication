import sys
from typing import Callable

class LoadScroller:
    """Print horizontal dots until stop condition"""

    def __init__(self, condition_check: Callable[[], bool]=lambda: True, frequency: int=1):
        if frequency < 1:
            raise ValueError('Frequency must be greater than 1')
        self.condition_check = condition_check
        self.toggled = False
        self._frequency = frequency
        self._count = 0

    def scroll(self) -> None:
        if not self.condition_check():
            return
        self._count += 1
        if self._count >= self._frequency:
            self._count = 0
            print('.', end='', flush=True, file=sys.stderr)