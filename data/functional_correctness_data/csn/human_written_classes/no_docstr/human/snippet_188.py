import moderngl
import os

class NoiseTexture:

    def __init__(self, width, height):
        self.ctx = moderngl.get_context()
        pixels = os.urandom(width * height * 3)
        self.texture = self.ctx.texture((width, height), 3, pixels)
        self.sampler = self.ctx.sampler(texture=self.texture)
        self.sampler.filter = (self.ctx.NEAREST, self.ctx.NEAREST)

    def use(self):
        self.sampler.use()