
class _Flake:
    '''
    Track a single snow flake.
    '''

    def __init__(self, screen: Screen):
        self.screen = screen
        self.x = random.randint(0, screen.width)
        self.y = random.randint(0, screen.height)
        self.speed = random.uniform(0.5, 2.0)
        self.size = random.randint(1, 3)
        self.color = (255, 255, 255)

    def _reseed(self):
        self.x = random.randint(0, self.screen.width)
        self.y = 0
        self.speed = random.uniform(0.5, 2.0)
        self.size = random.randint(1, 3)

    def update(self, reseed: bool):
        '''
        Update that snowflake!
        :param reseed: Whether we are in the normal reseed cycle or not.
        '''
        self.y += self.speed
        if self.y > self.screen.height or reseed:
            self._reseed()
