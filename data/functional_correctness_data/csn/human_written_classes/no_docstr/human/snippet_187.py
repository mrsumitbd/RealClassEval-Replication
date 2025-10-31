import numpy as np
import moderngl

class TriangleGeometry:

    def __init__(self):
        self.ctx = moderngl.get_context()
        vertices = np.array([0.0, 0.4, 0.0, -0.4, -0.3, 0.0, 0.4, -0.3, 0.0])
        self.vbo = self.ctx.buffer(vertices.astype('f4').tobytes())

    def vertex_array(self, program):
        return self.ctx.vertex_array(program, [(self.vbo, '3f', 'in_vertex')])