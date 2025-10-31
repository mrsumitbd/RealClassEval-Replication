
import random


class _Star:
    """
    A simple star that moves around a Screen, cycling through a given pattern.
    """

    def __init__(self, screen, pattern: str):
        """
        :param screen: The Screen being used for the Scene.
        :param pattern: The pattern to loop through
        """
        self.screen = screen
        self.pattern = pattern
        self.index = 0
        self.x = None
        self.y = None
        self.prev_char = None
        self._respawn()

    def _respawn(self):
        """
        Pick a random location for the star making sure it does
        not overwrite an existing piece of text.
        """
        # If the screen has a method to check occupancy, use it.
        # Otherwise, assume any position is free.
        max_attempts = 1000
        for _ in range(max_attempts):
            x = random.randint(0, self.screen.width - 1)
            y = random.randint(0, self.screen.height - 1)
            if hasattr(self.screen, "is_occupied"):
                if not self.screen.is_occupied(x, y):
                    break
            else:
                # Assume free if no method provided
                break
        else:
            # Fallback: just use the last tried position
            x = random.randint(0, self.screen.width - 1)
            y = random.randint(0, self.screen.height - 1)

        # Clear previous position if any
        if self.x is not None and self.y is not None:
            if hasattr(self.screen, "clear_char"):
                self.screen.clear_char(self.x, self.y)
            else:
                self.screen.set_char(self.x, self.y, " ")

        self.x, self.y = x, y
        self.prev_char = None

    def update(self):
        """
        Advance the star's pattern and render it on the screen.
        """
        if not self.pattern:
            return

        # Clear previous character
        if self.x is not None and self.y is not None:
            if hasattr(self.screen, "clear_char"):
                self.screen.clear_char(self.x, self.y)
            else:
                self.screen.set_char(self.x, self.y, " ")

        # Draw current character
        char = self.pattern[self.index]
        if hasattr(self.screen, "set_char"):
            self.screen.set_char(self.x, self.y, char)
        else:
            # Fallback: assume screen has a buffer we can index
            self.screen.buffer[self.y][self.x] = char

        # Advance pattern index
        self.index = (self.index + 1) % len(self.pattern)
