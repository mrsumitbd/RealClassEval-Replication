
import random


class Screen:
    # Assuming Screen class has a method to get its dimensions
    def get_dimensions(self):
        # For demonstration purposes, let's assume the screen dimensions are 800x600
        return 800, 600


class _Flake:

    def __init__(self, screen: Screen):
        self.screen = screen
        self.width, self.height = self.screen.get_dimensions()
        self.x = random.uniform(0, self.width)
        self.y = random.uniform(0, self.height)
        self.velocity_x = random.uniform(-0.5, 0.5)
        self.velocity_y = random.uniform(0.5, 2)
        self.size = random.uniform(1, 5)

    def _reseed(self):
        self.x = random.uniform(0, self.width)
        self.y = 0
        self.velocity_x = random.uniform(-0.5, 0.5)
        self.velocity_y = random.uniform(0.5, 2)
        self.size = random.uniform(1, 5)

    def update(self, reseed: bool):
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.y > self.height:
            if reseed:
                self._reseed()
            else:
                self.y = self.height


# Example usage
if __name__ == "__main__":
    screen = Screen()
    flake = _Flake(screen)
    for _ in range(100):
        flake.update(True)
        print(f"X: {flake.x}, Y: {flake.y}")
