
import random


class _Trail:
    '''
    Track a single trail for a falling character effect (a la Matrix).
    '''

    def __init__(self, screen, x: int):
        self.screen = screen
        self.x = x
        self.height = screen.height
        self.chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*"
        self._maybe_reseed(normal=False)

    def _maybe_reseed(self, normal: bool):
        if normal:
            # 1 in 20 chance to reseed
            if random.randint(0, 19) != 0:
                return
        self.length = random.randint(4, self.height // 2)
        self.y = random.randint(-self.height, 0)
        self.speed = random.randint(1, 2)
        self.trail = [random.choice(self.chars) for _ in range(self.length)]

    def update(self, reseed: bool):
        '''
        Update that trail!
        :param reseed: Whether we are in the normal reseed cycle or not.
        '''
        self._maybe_reseed(normal=reseed)
        # Erase the last character if it's on screen
        tail_y = self.y - 1
        if 0 <= tail_y < self.height:
            self.screen.addch(tail_y, self.x, ' ')
        # Draw the trail
        for i in range(self.length):
            char_y = self.y - i
            if 0 <= char_y < self.height:
                ch = self.trail[i] if i < len(
                    self.trail) else random.choice(self.chars)
                self.screen.addch(char_y, self.x, ch)
        # Move the trail down
        self.y += self.speed
        if self.y - self.length > self.height:
            self._maybe_reseed(normal=False)
