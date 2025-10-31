import moderngl
import math
import pygame

class Scene:

    def __init__(self):
        self.ctx = moderngl.get_context()

    def render(self):
        now = pygame.time.get_ticks() / 1000.0
        r = math.sin(now + 0.0) * 0.5 + 0.5
        g = math.sin(now + 2.1) * 0.5 + 0.5
        b = math.sin(now + 4.2) * 0.5 + 0.5
        self.ctx.clear(r, g, b)