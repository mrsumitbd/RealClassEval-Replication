
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
        self.screen = screen
        self.pattern = pattern
        self.index = 0
        self.x = 0
        self.y = 0
        self._respawn()

    def _respawn(self):
        '''
        Pick a random location for the star making sure it does
        not overwrite an existing piece of text.
        '''
        max_x = getattr(self.screen, 'width', 80)
        max_y = getattr(self.screen, 'height', 24)

        while True:
            x = random.randint(0, max_x - 1)
            y = random.randint(0, max_y - 1)
            # Assume screen has a method get_char that returns the character at (x, y)
            try:
                current = self.screen.get_char(x, y)
            except AttributeError:
                # Fallback: treat any attribute error as empty space
                current = ' '
            if current in (' ', None):
                self.x = x
                self.y = y
                break

    def update(self):
        '''
        Draw the star.
        '''
        ch = self.pattern[self.index]
        # Assume screen has a method set_char that sets the character at (x, y)
        try:
            self.screen.set_char(self.x, self.y, ch)
        except AttributeError:
            # If screen doesn't support set_char, ignore
            pass
        self.index = (self.index + 1) % len(self.pattern)
