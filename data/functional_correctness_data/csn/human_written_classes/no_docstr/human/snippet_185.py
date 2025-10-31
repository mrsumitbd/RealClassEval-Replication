import numpy as np
import moderngl

class PlaneGeometry:

    def __init__(self):
        self.ctx = moderngl.get_context()
        vertices = np.array([-0.5, -0.5, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.5, -0.5, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, -0.5, 0.5, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, -0.5, 0.5, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.5, -0.5, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0])
        self.vbo = self.ctx.buffer(vertices.astype('f4').tobytes())

    def vertex_array(self, program):
        return self.ctx.vertex_array(program, [(self.vbo, '3f 12x 8x', 'in_vertex')])