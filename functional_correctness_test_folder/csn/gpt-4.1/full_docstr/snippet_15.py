
import random


class _Star:
    '''
    Simple class to represent a single star for the Stars special effect.
    '''

    def __init__(self, screen, pattern: str):
        '''
        :param screen: The Screen being used for the Scene.
        :param pattern: The pattern to loop through
        '''
        self._screen = screen
        self._pattern = pattern
        self._pattern_len = len(pattern)
        self._frame = random.randint(0, self._pattern_len - 1)
        self._respawn()

    def _respawn(self):
        '''
        Pick a random location for the star making sure it does
        not overwrite an existing piece of text.
        '''
        height = self._screen.height
        width = self._screen.width
        while True:
            self._x = random.randint(0, width - 1)
            self._y = random.randint(0, height - 1)
            # Check if the cell is empty (assuming get_from returns a tuple (char, attr, colour, bg))
            cell = self._screen.get_from(self._x, self._y)
            if cell[0] == " ":
                break

    def update(self):
        '''
        Draw the star.
        '''
        # Draw the current pattern character at the star's position
        self._screen.print_at(
            self._pattern[self._frame],
            self._x,
            self._y
        )
        # Advance the frame
        self._frame = (self._frame + 1) % self._pattern_len
