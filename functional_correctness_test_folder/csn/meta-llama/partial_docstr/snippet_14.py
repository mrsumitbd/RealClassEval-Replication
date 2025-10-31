
import random


class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class _Flake:
    '''
    Track a single snow flake.
    '''

    def __init__(self, screen: Screen):
        self.screen = screen
        self.x = random.uniform(0, screen.width)
        self.y = random.uniform(0, screen.height)
        self.speed_x = random.uniform(-0.5, 0.5)
        self.speed_y = random.uniform(0.5, 2)

    def _reseed(self):
        self.x = random.uniform(0, self.screen.width)
        self.y = 0
        self.speed_x = random.uniform(-0.5, 0.5)
        self.speed_y = random.uniform(0.5, 2)

    def update(self, reseed: bool):
        '''
        Update that snowflake!
        :param reseed: Whether we are in the normal reseed cycle or not.
        '''
        self.x += self.speed_x
        self.y += self.speed_y

        if self.y > self.screen.height:
            if reseed:
                self._reseed()
            else:
                self.y = 0

        if self.x < 0 or self.x > self.screen.width:
            self.speed_x *= -1

# Example usage:


def main():
    screen = Screen(800, 600)
    flake = _Flake(screen)

    for _ in range(100):
        flake.update(True)
        print(f"X: {flake.x}, Y: {flake.y}")


if __name__ == "__main__":
    main()
