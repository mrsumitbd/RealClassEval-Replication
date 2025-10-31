import moderngl
import math
import pygame

class Scene:

    def __init__(self):
        self.ctx = moderngl.get_context()
        self.uniform_buffer = UniformBuffer()
        self.texture = ImageTexture('examples/data/textures/crate.png')
        self.color_material = ColorMaterial()
        self.texture_material = TextureMaterial(self.texture)
        self.car_geometry = ModelGeometry('examples/data/models/lowpoly_toy_car.obj')
        self.car = Mesh(self.color_material, self.car_geometry)
        self.crate_geometry = ModelGeometry('examples/data/models/crate.obj')
        self.crate = Mesh(self.texture_material, self.crate_geometry)

    def render(self):
        now = pygame.time.get_ticks() / 1000.0
        eye = (math.cos(now), math.sin(now), 0.5)
        self.ctx.clear()
        self.ctx.enable(self.ctx.DEPTH_TEST)
        self.uniform_buffer.set_camera(eye, (0.0, 0.0, 0.0))
        self.uniform_buffer.set_light_direction(1.0, 2.0, 3.0)
        self.uniform_buffer.use()
        self.crate.render((0.0, 0.0, 0.0), 0.2)
        self.color_material.color = (1.0, 0.0, 0.0)
        self.car.render((-0.4, 0.0, 0.0), 0.2)
        self.color_material.color = (0.0, 0.0, 1.0)
        self.car.render((0.4, 0.0, 0.0), 0.2)