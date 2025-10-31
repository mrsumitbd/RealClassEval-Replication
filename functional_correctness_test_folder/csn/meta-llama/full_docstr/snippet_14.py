
import random


class Screen:  # Assuming this is defined elsewhere, but for completeness...
    def __init__(self, width, height):
        self.width = width
        self.height = height


class _Flake:
    '''
    Track a single snow flake.
    '''

    def __init__(self, screen: Screen):
        '''
        :param screen: The Screen being used for the Scene.
        '''
        self.screen = screen
        self.x = random.uniform(0, screen.width)
        self.y = random.uniform(-50, -10)
        self.vel_x = random.uniform(-0.5, 0.5)
        self.vel_y = random.uniform(0.5, 2)
        self.size = random.uniform(2, 5)

    def _reseed(self):
        '''
        Randomly create a new snowflake once this one is finished.
        '''
        self.x = random.uniform(0, self.screen.width)
        self.y = random.uniform(-50, -10)
        self.vel_x = random.uniform(-0.5, 0.5)
        self.vel_y = random.uniform(0.5, 2)
        self.size = random.uniform(2, 5)

    def update(self, reseed: bool):
        '''
        Update that snowflake!
        :param reseed: Whether we are in the normal reseed cycle or not.
        '''
        self.x += self.vel_x
        self.y += self.vel_y

        if self.y > self.screen.height:
            if reseed:
                self._reseed()
            else:
                self.y = -10  # Keep it off-screen


# Example usage:
if __name__ == "__main__":
    screen = Screen(800, 600)
    flake = _Flake(screen)
    for _ in range(100):
        flake.update(True)
        print(f"X: {flake.x}, Y: {flake.y}")
