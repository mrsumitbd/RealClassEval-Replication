import glm
import math
import pygame
import moderngl

class Scene:

    def __init__(self):
        self.ctx = moderngl.get_context()
        self.program = self.ctx.program(vertex_shader='\n                #version 330 core\n\n                uniform mat4 camera;\n                uniform vec3 position;\n                uniform float scale;\n\n                layout (location = 0) in vec3 in_vertex;\n\n                void main() {\n                    gl_Position = camera * vec4(position + in_vertex * scale, 1.0);\n                }\n            ', fragment_shader='\n                #version 330 core\n\n                uniform vec3 color;\n\n                layout (location = 0) out vec4 out_color;\n\n                void main() {\n                    out_color = vec4(color, 1.0);\n                }\n            ')
        self.triangle_geometry = TriangleGeometry()
        self.triangle = Mesh(self.program, self.triangle_geometry)

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
        self.program['camera'].write(camera)
        self.triangle.render((-0.2, 0.0, 0.0), (1.0, 0.0, 0.0), 0.2)
        self.triangle.render((0.0, 0.0, 0.0), (0.0, 1.0, 0.0), 0.2)
        self.triangle.render((0.2, 0.0, 0.0), (0.0, 0.0, 1.0), 0.2)