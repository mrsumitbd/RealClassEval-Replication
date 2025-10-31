
import random


class _Star:

    def __init__(self, screen, pattern: str):
        '''
        :param screen: The Screen being used for the Scene.
        :param pattern: The pattern to loop through
        '''
        self.screen = screen
        self.pattern = pattern
        self.pattern_index = 0
        self.x = 0
        self.y = 0
        self._respawn()

    def _respawn(self):
        '''
        Pick a random location for the star making sure it does
        not overwrite an existing piece of text.
        '''
        max_attempts = 100
        for _ in range(max_attempts):
            x = random.randint(0, self.screen.width - 1)
            y = random.randint(0, self.screen.height - 1)
            # Check if the cell is empty (assuming None or ' ' is empty)
            if self.screen.get_from(x, y) in (None, ' '):
                self.x = x
                self.y = y
                return
        # If no empty cell found, just pick a random one
        self.x = random.randint(0, self.screen.width - 1)
        self.y = random.randint(0, self.screen.height - 1)

    def update(self):
        # Erase previous star
        self.screen.print_at(' ', self.x, self.y)
        # Move star down
        self.y += 1
        if self.y >= self.screen.height:
            self._respawn()
            self.y = 0
        # Draw star with current pattern character
        char = self.pattern[self.pattern_index]
        self.screen.print_at(char, self.x, self.y)
        self.pattern_index = (self.pattern_index + 1) % len(self.pattern)
