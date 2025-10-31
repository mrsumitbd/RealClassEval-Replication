
import random
from typing import Any


class _Flake:
    """
    A simple snowflake simulation object.

    The class expects the `screen` argument to expose `width` and `height`
    attributes that define the drawing area.  The flake is represented by
    a position, a falling speed, a size, and an opacity.  The flake
    automatically re‑spawns when it moves past the bottom of the screen.
    """

    def __init__(self, screen: Any):
        """
        Initialise a new flake.

        Parameters
        ----------
        screen : Any
            An object that provides `width` and `height` attributes.
        """
        self.screen = screen
        self._reseed()

    def _reseed(self):
        """
        Randomise the flake's starting position and visual properties.
        """
        # Position: start somewhere above the visible area
        self.x = random.uniform(0, self.screen.width)
        self.y = random.uniform(-self.screen.height, 0)

        # Falling speed (pixels per update)
        self.speed = random.uniform(1.0, 3.0)

        # Size (used for drawing and wrap‑around)
        self.size = random.randint(1, 3)

        # Opacity (0.0 to 1.0)
        self.opacity = random.uniform(0.5, 1.0)

        # Optional horizontal drift
        self.drift = random.uniform(-0.5, 0.5)

    def update(self, reseed: bool):
        """
        Move the flake downwards and optionally reseed it when it leaves
        the screen.

        Parameters
        ----------
        reseed : bool
            If True, the flake will be reseeded when it moves past the
            bottom of the screen.  If False, it will simply wrap to the
            top.
        """
        # Apply vertical movement
        self.y += self.speed

        # Apply horizontal drift
        self.x += self.drift

        # Keep the flake within horizontal bounds
        if self.x < 0:
            self.x += self.screen.width
        elif self.x > self.screen.width:
            self.x -= self.screen.width

        # If the flake has fallen below the screen
        if self.y > self.screen.height:
            if reseed:
                self._reseed()
            else:
                # Wrap to the top
                self.y = -self.size
