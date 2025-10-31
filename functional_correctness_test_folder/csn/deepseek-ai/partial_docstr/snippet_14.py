
class _Flake:
    '''
    Track a single snow flake.
    '''

    def __init__(self, screen: Screen):
        self.screen = screen
        self.x = 0
        self.y = 0
        self._reseed()

    def _reseed(self):
        import random
        self.x = random.randint(0, self.screen.width - 1)
        self.y = random.randint(-10, -1)
        self.speed = random.uniform(0.5, 2.0)

    def update(self, reseed: bool):
        '''
        Update that snowflake!
        :param reseed: Whether we are in the normal reseed cycle or not.
        '''
        self.y += self.speed
        if self.y >= self.screen.height or reseed:
            self._reseed()
