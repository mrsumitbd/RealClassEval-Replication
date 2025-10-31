import moderngl

class Mesh:

    def __init__(self, program, geometry):
        self.ctx = moderngl.get_context()
        self.vao = geometry.vertex_array(program)

    def render(self, position, color, scale):
        self.vao.program['position'] = position
        self.vao.program['color'] = color
        self.vao.program['scale'] = scale
        self.vao.render()