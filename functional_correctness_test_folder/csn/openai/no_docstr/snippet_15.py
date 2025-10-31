
import random


class _Star:
    """
    A simple star that moves leftwards across a screen and respawns on the right edge.
    The star cycles through the characters in `pattern` each frame.
    """

    def __init__(self, screen: "Screen", pattern: str):
        """
        Parameters
        ----------
        screen : Screen
            The screen object that provides width, height and a method to draw characters.
        pattern : str
            A string of characters that the star cycles through.
        """
        self.screen = screen
        self.pattern = pattern
        self.index = 0  # current character index in the pattern
        self.x = 0
        self.y = 0
        self._respawn()

    def _respawn(self):
        """
        Place the star at a random vertical position on the rightmost column of the screen.
        """
        # Use the screen's width and height attributes if available
        width = getattr(self.screen, "width", None)
        height = getattr(self.screen, "height", None)

        if width is None or height is None:
            raise AttributeError(
                "Screen object must have 'width' and 'height' attributes")

        self.x = width - 1
        self.y = random.randint(0, height - 1)

    def update(self):
        """
        Draw the star at its current position, advance its character, and move it left.
        If it moves off the screen, respawn it on the right.
        """
        # Determine the drawing method
        draw_method = getattr(self.screen, "draw", None)
        if draw_method is None:
            draw_method = getattr(self.screen, "put", None)
        if draw_method is None:
            raise AttributeError(
                "Screen object must have a 'draw' or 'put' method")

        # Draw the current character
        char = self.pattern[self.index % len(self.pattern)]
        draw_method(self.x, self.y, char)

        # Advance to the next character in the pattern
        self.index += 1

        # Move left
        self.x -= 1

        # If the star has moved off the left edge, respawn it
        if self.x < 0:
            self._respawn()
