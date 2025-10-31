import moderngl

class Mesh:

    def __init__(self, material, geometry):
        self.ctx = moderngl.get_context()
        self.vao = material.vertex_array(geometry.vbo)
        self.material = material

    def render(self, position, scale):
        self.material.use()
        self.vao.program['position'] = position
        self.vao.program['scale'] = scale
        self.vao.render()