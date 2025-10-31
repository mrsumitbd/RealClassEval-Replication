import pygame
import moderngl
import math
import glm

class Scene:

    def __init__(self):
        self.ctx = moderngl.get_context()
        self.texture = ImageTexture('examples/data/textures/crate.png')
        self.color_material = ColorMaterial()
        self.texture_material = TextureMaterial(self.texture)
        self.car_geometry = ModelGeometry('examples/data/models/lowpoly_toy_car.obj')
        self.car = Mesh(self.color_material, self.car_geometry)
        self.crate_geometry = ModelGeometry('examples/data/models/crate.obj')
        self.crate = Mesh(self.texture_material, self.crate_geometry)

    def camera_matrix(self):
        now = pygame.time.get_ticks() / 1000.0
        eye = (math.cos(now), math.sin(now), 0.5)
        proj = glm.perspective(45.0, 1.0, 0.1, 1000.0)
        look = glm.lookAt(eye, (0.0, 0.0, 0.0), (0.0, 0.0, 1.0))
        return proj * look

    def render(self):
        camera = self.camera_matrix()
        self.ctx.clear()
        self.ctx.enable(self.ctx.DEPTH_TEST)
        self.color_material.program['camera'].write(camera)
        self.color_material.program['light_direction'] = (1.0, 2.0, 3.0)
        self.texture_material.program['camera'].write(camera)
        self.texture_material.program['light_direction'] = (1.0, 2.0, 3.0)
        self.crate.render((0.0, 0.0, 0.0), 0.2)
        self.color_material.color = (1.0, 0.0, 0.0)
        self.car.render((-0.4, 0.0, 0.0), 0.2)
        self.color_material.color = (0.0, 0.0, 1.0)
        self.car.render((0.4, 0.0, 0.0), 0.2)