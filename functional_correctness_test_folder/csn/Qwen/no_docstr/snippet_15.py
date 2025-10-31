
class _Star:

    def __init__(self, screen: Screen, pattern: str):
        self.screen = screen
        self.pattern = pattern
        # Example position, can be initialized differently
        self.position = (0, 0)
        self._respawn()

    def _respawn(self):
        import random
        width, height = self.screen.get_size()
        self.position = (random.randint(0, width), random.randint(0, height))

    def update(self):
        x, y = self.position
        width, height = self.screen.get_size()
        self.position = (x + 1, y)  # Example movement, can be customized
        if x > width:
            self._respawn()
        self.screen.draw(self.position, self.pattern)
