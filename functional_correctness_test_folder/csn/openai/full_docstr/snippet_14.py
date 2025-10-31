
import random


class _Flake:
    '''
    Track a single snow flake.
    '''

    def __init__(self, screen: 'Screen'):
        '''
        :param screen: The Screen being used for the Scene.
        '''
        self.screen = screen
        self._reseed()

    def _reseed(self):
        '''
        Randomly create a new snowflake once this one is finished.
        '''
        # Position: start somewhere above the screen
        self.x = random.uniform(0, self.screen.width)
        self.y = random.uniform(-self.screen.height, 0)

        # Speed: how fast it falls
        self.speed = random.uniform(0.5, 2.0)

        # Size: radius of the flake
        self.size = random.uniform(1.0, 3.0)

        # Optional: color (white)
        self.color = (255, 255, 255)

    def update(self, reseed: bool):
        '''
        Update that snowflake!
        :param reseed: Whether we are in the normal reseed cycle or not.
        '''
        # Move the flake downwards
        self.y += self.speed

        # If it has fallen below the screen
        if self.y - self.size > self.screen.height:
            if reseed:
                self._reseed()
            else:
                # Just wrap it back to the top
                self.y = -self.size
                self.x = random.uniform(0, self.screen.width)
