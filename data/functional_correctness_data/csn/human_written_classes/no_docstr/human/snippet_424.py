import pygame
import esper

class RenderProcessor:

    def __init__(self, window, clear_color=(0, 0, 0)):
        super().__init__()
        self.window = window
        self.clear_color = clear_color

    def process(self):
        self.window.fill(self.clear_color)
        for ent, rend in esper.get_component(Renderable):
            self.window.blit(rend.image, (rend.x, rend.y))
        pygame.display.flip()