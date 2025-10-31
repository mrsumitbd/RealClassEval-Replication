import moderngl

class Scene:

    def __init__(self):
        self.ctx = moderngl.get_context()
        self.program = self.ctx.program(vertex_shader='\n                #version 330 core\n\n                vec3 vertices[3] = vec3[](\n                    vec3(0.0, 0.4, 0.0),\n                    vec3(-0.4, -0.3, 0.0),\n                    vec3(0.4, -0.3, 0.0)\n                );\n\n                void main() {\n                    gl_Position = vec4(vertices[gl_VertexID], 1.0);\n                }\n            ', fragment_shader='\n                #version 330 core\n\n                layout (location = 0) out vec4 out_color;\n\n                void main() {\n                    out_color = vec4(1.0, 1.0, 1.0, 1.0);\n                }\n            ')
        self.vao = self.ctx.vertex_array(self.program, [])
        self.vao.vertices = 3

    def render(self):
        self.ctx.clear()
        self.vao.render()