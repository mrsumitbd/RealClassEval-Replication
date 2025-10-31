
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
        self._respawn()

    def _respawn(self):
        '''
        Pick a random location for the star making sure it does
        not overwrite an existing piece of text.
        '''
        max_x, max_y = self.screen.getmaxyx()
        while True:
            self.x = random.randint(0, max_x - 1)
            self.y = random.randint(0, max_y - 1)
            if self.screen.inch(self.y, self.x) == ord(' '):
                break

    def update(self):
        '''
        Draw the star.
        '''
        char = self.pattern[self.index]
        self.screen.addch(self.y, self.x, char)
        self.index = (self.index + 1) % len(self.pattern)
