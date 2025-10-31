
import random
from typing import List, Tuple


class _Trail:
    """
    Track a single trail for a falling character effect (a la Matrix).
    """
    # Characters used in the trail
    _CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*"

    def __init__(self, screen, x: int):
        """
        :param screen: The screen object that provides a put_char(x, y, char, color) method.
        :param x: The horizontal position of the trail.
        """
        self.screen = screen
        self.x = x
        self.height = getattr(screen, "height", 24)  # fallback height
        self._reset()

    def _reset(self):
        """Reset the trail to a new random length and clear its state."""
        self.length = random.randint(5, max(5, self.height // 2))
        self.head_y = -1  # start above the screen
        self.chars: List[str] = []  # characters in the trail (head first)
        # No need to keep colors separately; we compute them on the fly

    def _maybe_reseed(self, normal: bool):
        """
        Possibly reseed the trail. If normal is True, reseed with a small probability.
        If normal is False, reseed immediately.
        """
        if normal:
            # 2% chance to reseed each update
            if random.random() < 0.02:
                self._reset()
        else:
            self._reset()

    def update(self, reseed: bool):
        """
        Update that trail!
        :param reseed: Whether we are in the normal reseed cycle or not.
        """
        # Move the head down
        self.head_y += 1

        # If the head has moved past the bottom, reseed
        if self.head_y >= self.height:
            self._maybe_reseed(normal=reseed)
            return

        # Generate a new character for the head
        new_char = random.choice(self._CHARS)
        self.chars.insert(0, new_char)

        # Trim the trail to its maximum length
        if len(self.chars) > self.length:
            self.chars.pop()

        # Draw the trail
        for idx, char in enumerate(self.chars):
            y = self.head_y - idx
            if 0 <= y < self.height:
                # Brightness: head is bright, tail is dimmer
                if idx == 0:
                    color = 0x00FF00  # bright green
                else:
                    color = 0x004400  # dim green
                # Assume the screen has a put_char method
                self.screen.put_char(self.x, y, char, color)
