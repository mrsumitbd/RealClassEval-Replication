
class _Flake:

    def __init__(self, screen: Screen):
        self.screen = screen
        self._reseed()

    def _reseed(self):
        import random
        self.x = random.randint(0, self.screen.width - 1)
        self.y = random.randint(-10, -1)
        self.speed = random.uniform(0.5, 2.0)

    def update(self, reseed: bool):
        self.y += self.speed
        if reseed or self.y >= self.screen.height:
            self._reseed()
