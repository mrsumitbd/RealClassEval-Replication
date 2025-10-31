
class _Trail:
    '''
    Track a single trail  for a falling character effect (a la Matrix).
    '''

    def __init__(self, screen: Screen, x: int):
        self.screen = screen
        self.x = x
        self.y = 0
        self.length = 0
        self.max_length = 10
        self.reseed_rate = 0.05
        self._maybe_reseed(normal=True)

    def _maybe_reseed(self, normal: bool):
        if normal:
            if random.random() < self.reseed_rate:
                self._reseed()
        else:
            self._reseed()

    def _reseed(self):
        self.y = 0
        self.length = random.randint(1, self.max_length)

    def update(self, reseed: bool):
        '''
        Update that trail!
        :param reseed: Whether we are in the normal reseed cycle or not.
        '''
        self._maybe_reseed(normal=not reseed)
        if self.y < self.screen.height:
            self.y += 1
        else:
            self._reseed()

        # Clear the previous trail
        for i in range(self.length):
            if self.y - i - 1 >= 0:
                self.screen.set_char(self.x, self.y - i - 1, ' ')

        # Draw the new trail
        for i in range(self.length):
            if self.y - i >= 0:
                self.screen.set_char(self.x, self.y - i,
                                     chr(random.randint(33, 126)))
