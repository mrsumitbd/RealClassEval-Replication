
import random


class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class _Star:

    def __init__(self, screen: Screen, pattern: str):
        self.screen = screen
        self.pattern = pattern
        self.x = random.randint(0, screen.width)
        self.y = random.randint(0, screen.height)
        self.speed = random.uniform(0.1, 2.0)

    def _respawn(self):
        self.x = random.randint(0, self.screen.width)
        self.y = 0

    def update(self):
        self.y += self.speed
        if self.y > self.screen.height:
            self._respawn()


# Example usage:
if __name__ == "__main__":
    screen = Screen(800, 600)
    star = _Star(screen, "*")
    for _ in range(100):
        star.update()
        print(f"Star position: ({star.x}, {star.y})")
