
import random
import string
from typing import List, Tuple


class _Trail:
    '''
    Track a single trail  for a falling character effect (a la Matrix).
    '''

    def __init__(self, screen, x: int):
        '''
        :param screen: The Screen being used for the Scene.
        :param x: The column (y coordinate) for this trail to use.
        '''
        self.screen = screen
        self.x = x
        self.positions: List[int] = []          # y positions of each character
        self.chars: List[str] = []              # characters in the trail
        self._maybe_reseed(normal=True)        # start with a fresh trail

    def _maybe_reseed(self, normal: bool):
        '''
        Randomly create a new column once this one is finished.
        '''
        if normal:
            # Random length between 5 and 15 characters
            length = random.randint(5, 15)
            # Generate random characters (letters and digits)
            self.chars = [random.choice(
                string.ascii_letters + string.digits) for _ in range(length)]
            # All start at the top (y = 0)
            self.positions = [0] * length
        else:
            # In non‑normal mode we simply clear the trail
            self.chars = []
            self.positions = []

    def update(self, reseed: bool):
        '''
        Update that trail!
        :param reseed: Whether we are in the normal reseed cycle or not.
        '''
        new_positions: List[int] = []
        new_chars: List[str] = []

        # Move each character down by one row
        for y, ch in zip(self.positions, self.chars):
            new_y = y + 1
            if new_y <= self.screen.height:
                # Draw the character at the new position
                # Assume screen.put_char(x, y, char, color)
                try:
                    self.screen.put_char(self.x, new_y, ch, 'green')
                except Exception:
                    # If the screen API differs, ignore drawing errors
                    pass
                new_positions.append(new_y)
                new_chars.append(ch)

        self.positions = new_positions
        self.chars = new_chars

        # If the trail is finished, reseed it
        if not self.positions:
            self._maybe_reseed(normal=reseed)
