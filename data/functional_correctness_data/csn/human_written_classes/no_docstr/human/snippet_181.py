import moderngl
import pygame
import glm
import math
import numpy as np

class Scene:

    def __init__(self):
        self.ctx = moderngl.get_context()
        self.program = self.ctx.program(vertex_shader='\n                #version 330 core\n\n                uniform mat4 camera;\n\n                layout (location = 0) in vec3 in_vertex;\n\n                void main() {\n                    gl_Position = camera * vec4(in_vertex, 1.0);\n                }\n            ', fragment_shader='\n                #version 330 core\n\n                layout (location = 0) out vec4 out_color;\n\n                void main() {\n                    out_color = vec4(1.0, 1.0, 1.0, 1.0);\n                }\n            ')
        vertices = np.array([0.0, 0.4, 0.0, -0.4, -0.3, 0.0, 0.4, -0.3, 0.0])
        self.vbo = self.ctx.buffer(vertices.astype('f4').tobytes())
        self.vao = self.ctx.vertex_array(self.program, [(self.vbo, '3f', 'in_vertex')])

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
        self.vao.render()