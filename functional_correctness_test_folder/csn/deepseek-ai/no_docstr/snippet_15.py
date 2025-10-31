
class _Star:

    def __init__(self, screen: Screen, pattern: str):
        self.screen = screen
        self.pattern = pattern
        self._respawn()

    def _respawn(self):
        self.x = random.randint(0, self.screen.width)
        self.y = random.randint(0, self.screen.height)
        self.speed = random.uniform(0.5, 2.0)

    def update(self):
        self.y += self.speed
        if self.y > self.screen.height:
            self._respawn()
