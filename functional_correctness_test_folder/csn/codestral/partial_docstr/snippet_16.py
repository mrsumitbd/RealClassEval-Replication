
class _Trail:
    '''
    Track a single trail  for a falling character effect (a la Matrix).
    '''

    def __init__(self, screen: Screen, x: int):
        self.screen = screen
        self.x = x
        self.y = 0
        self.length = random.randint(5, 20)
        self.speed = random.uniform(0.1, 0.5)
        self.characters = [chr(random.randint(33, 126))
                           for _ in range(self.length)]
        self.head_color = (0, 255, 0)
        self.tail_color = (0, 100, 0)

    def _maybe_reseed(self, normal: bool):
        if normal:
            if self.y >= self.screen.height or random.random() < 0.01:
                self.y = 0
                self.length = random.randint(5, 20)
                self.speed = random.uniform(0.1, 0.5)
                self.characters = [chr(random.randint(33, 126))
                                   for _ in range(self.length)]
        else:
            if self.y >= self.screen.height or random.random() < 0.1:
                self.y = 0
                self.length = random.randint(5, 20)
                self.speed = random.uniform(0.1, 0.5)
                self.characters = [chr(random.randint(33, 126))
                                   for _ in range(self.length)]

    def update(self, reseed: bool):
        '''
        Update that trail!
        :param reseed: Whether we are in the normal reseed cycle or not.
        '''
        self._maybe_reseed(reseed)
        self.y += self.speed
        for i in range(self.length):
            y_pos = int(self.y - i)
            if 0 <= y_pos < self.screen.height:
                color = self._get_color(i)
                self.screen.draw_char(self.x, y_pos, self.characters[i], color)

    def _get_color(self, index: int):
        ratio = index / self.length
        r = int(self.head_color[0] * (1 - ratio) + self.tail_color[0] * ratio)
        g = int(self.head_color[1] * (1 - ratio) + self.tail_color[1] * ratio)
        b = int(self.head_color[2] * (1 - ratio) + self.tail_color[2] * ratio)
        return (r, g, b)
