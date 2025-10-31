
import random
import pygame


class _Flake:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.x = random.randint(0, screen.get_width())
        self.y = random.randint(0, screen.get_height())
        self.speed = random.uniform(0.1, 1.0)
        self.size = random.randint(1, 3)
        self.color = (255, 255, 255)

    def _reseed(self):
        self.x = random.randint(0, self.screen.get_width())
        self.y = 0
        self.speed = random.uniform(0.1, 1.0)
        self.size = random.randint(1, 3)

    def update(self, reseed: bool):
        if reseed or self.y > self.screen.get_height():
            self._reseed()
        else:
            self.y += self.speed

        pygame.draw.circle(self.screen, self.color,
                           (int(self.x), int(self.y)), self.size)
