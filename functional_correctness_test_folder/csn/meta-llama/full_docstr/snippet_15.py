
import random


class _Star:
    '''
    Simple class to represent a single star for the Stars special effect.
    '''

    def __init__(self, screen: 'Screen', pattern: str):
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
        while True:
            self.x = random.randint(0, self.screen.width - 1)
            self.y = random.randint(0, self.screen.height - 1)
            if self.screen.get_from(self.x, self.y) == (0, 0, 0):
                break

    def update(self):
        '''
        Draw the star.
        '''
        self.screen.print_at(self.pattern[self.index], self.x, self.y)
        self.index = (self.index + 1) % len(self.pattern)
