
import random


class _Star:

    def __init__(self, screen: 'Screen', pattern: str):
        '''
        :param screen: The Screen being used for the Scene.
        :param pattern: The pattern to loop through
        '''
        self.screen = screen
        self.pattern = pattern
        self.x = 0
        self.y = 0
        self.char_index = 0
        self._respawn()

    def _respawn(self):
        '''
        Pick a random location for the star making sure it does
        not overwrite an existing piece of text.
        '''
        height, width = self.screen.height, self.screen.width
        while True:
            self.x = random.randint(0, width - 1)
            self.y = random.randint(0, height - 1)
            if self.screen.get_from(self.x, self.y) == ' ':
                break

    def update(self):
        '''
        Update the star's position and character.
        '''
        self.screen.print_at(self.pattern[self.char_index], self.x, self.y)
        self.char_index = (self.char_index + 1) % len(self.pattern)
