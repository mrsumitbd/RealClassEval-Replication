
import random


class _Flake:
    '''
    Track a single snow flake.
    '''

    def __init__(self, screen):
        """
        Initialise a snowflake with a reference to the screen.
        The screen object is expected to expose `width` and `height` attributes.
        """
        self.screen = screen
        self._reseed()

    def _reseed(self):
        """
        Randomise the flake's position, speed and size.
        The flake starts somewhere above the visible area.
        """
        # Position: x anywhere across the width, y somewhere above the top
        self.x = random.uniform(0, self.screen.width)
        self.y = random.uniform(-self.screen.height, 0)

        # Speed: how many pixels per update tick
        self.speed = random.uniform(1.0, 3.0)

        # Size: radius in pixels (used for drawing)
        self.size = random.randint(1, 3)

    def update(self, reseed: bool):
        """
        Update that snowflake!
        :param reseed: Whether we are in the normal reseed cycle or not.
        """
        # Move the flake downwards
        self.y += self.speed

        # If it has fallen below the screen, either reseed or wrap
        if self.y > self.screen.height:
            if reseed:
                self._reseed()
            else:
                # Wrap to the top
                self.y = 0
                self.x = random.uniform(0, self.screen.width)
