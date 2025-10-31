
import random
from typing import List, Tuple


class _Trail:
    """
    A simple trail that keeps a list of characters at a fixed x position on a screen.
    Each update step moves the trail down by one row and optionally adds a new
    character at the top. The new character's vertical position can be chosen
    either from a normal distribution (if normal=True) or uniformly across the
    screen height.
    """

    def __init__(self, screen, x: int):
        """
        Parameters
        ----------
        screen : object
            The screen object. It must expose a `height` attribute and a
            `write(x, y, char)` method.
        x : int
            The fixed horizontal position of the trail.
        """
        self.screen = screen
        self.x = x
        self.segments: List[Tuple[int, str]] = []  # list of (y, char)
        # fallback if width not present
        self.max_length = getattr(screen, "width", 80)

    def _maybe_reseed(self, normal: bool):
        """
        Add a new segment at the top of the trail.

        Parameters
        ----------
        normal : bool
            If True, the y position is drawn from a normal distribution
            centered at half the screen height. If False, the y position
            is drawn uniformly from the screen height.
        """
        height = getattr(self.screen, "height", 24)
        if normal:
            # Normal distribution centered at middle with std dev of 1/4 height
            y = int(random.gauss(height / 2, height / 8))
        else:
            y = random.randint(0, height - 1)

        # Clamp y to screen bounds
        y = max(0, min(height - 1, y))

        # Choose a random character for the trail
        char = random.choice(".*+")
        self.segments.append((y, char))

        # Keep the trail length bounded
        if len(self.segments) > self.max_length:
            self.segments.pop(0)

    def update(self, reseed: bool):
        """
        Advance the trail by one step.

        Parameters
        ----------
        reseed : bool
            If True, a new segment is added at the top of the trail.
        """
        if reseed:
            self._maybe_reseed(normal=True)

        # Move all segments down by one row
        new_segments: List[Tuple[int, str]] = []
        for y, char in self.segments:
            new_y = y + 1
            if new_y < getattr(self.screen, "height", 24):
                new_segments.append((new_y, char))

        self.segments = new_segments

        # Draw the trail on the screen
        for y, char in self.segments:
            try:
                self.screen.write(self.x, y, char)
            except Exception:
                # If the screen object does not support write, ignore
                pass
