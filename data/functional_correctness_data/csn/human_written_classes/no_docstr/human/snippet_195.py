import moderngl

class ColorMaterial:

    def __init__(self):
        self.ctx = moderngl.get_context()
        self.program = self.ctx.program(vertex_shader='\n                #version 330 core\n\n                uniform mat4 camera;\n                uniform vec3 position;\n                uniform float scale;\n\n                layout (location = 0) in vec3 in_vertex;\n                layout (location = 1) in vec3 in_normal;\n                layout (location = 2) in vec2 in_uv;\n\n                out vec3 v_vertex;\n                out vec3 v_normal;\n                out vec2 v_uv;\n\n                void main() {\n                    v_vertex = position + in_vertex * scale;\n                    v_normal = in_normal;\n                    v_uv = in_uv;\n\n                    gl_Position = camera * vec4(v_vertex, 1.0);\n                }\n            ', fragment_shader='\n                #version 330 core\n\n                uniform vec3 light_direction;\n                uniform vec3 color;\n\n                in vec3 v_vertex;\n                in vec3 v_normal;\n                in vec2 v_uv;\n\n                layout (location = 0) out vec4 out_color;\n\n                void main() {\n                    out_color = vec4(color, 1.0);\n                    float lum = dot(normalize(v_normal), normalize(light_direction));\n                    out_color.rgb *= max(lum, 0.0) * 0.5 + 0.5;\n                }\n            ')
        self.color = (1.0, 1.0, 1.0)

    def use(self):
        self.program['color'] = self.color

    def vertex_array(self, buffer):
        return self.ctx.vertex_array(self.program, [(buffer, '3f 3f 8x', 'in_vertex', 'in_normal')])