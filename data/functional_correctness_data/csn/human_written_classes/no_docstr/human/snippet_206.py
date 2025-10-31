import moderngl

class ColorMaterial:

    def __init__(self):
        self.ctx = moderngl.get_context()
        self.program = self.ctx.program(vertex_shader='\n                #version 330 core\n                #include "uniform_buffer"\n\n                uniform vec3 position;\n                uniform float scale;\n\n                layout (location = 0) in vec3 in_vertex;\n                layout (location = 1) in vec3 in_normal;\n                layout (location = 2) in vec2 in_uv;\n\n                out vec3 v_vertex;\n                out vec3 v_normal;\n                out vec2 v_uv;\n\n                void main() {\n                    v_vertex = position + in_vertex * scale;\n                    v_normal = in_normal;\n                    v_uv = in_uv;\n\n                    gl_Position = camera * vec4(v_vertex, 1.0);\n                }\n            ', fragment_shader='\n                #version 330 core\n                #include "uniform_buffer"\n                #include "blinn_phong"\n                #include "calculate_lights"\n                #include "srgb"\n\n                uniform vec3 color;\n\n                in vec3 v_vertex;\n                in vec3 v_normal;\n                in vec2 v_uv;\n\n                layout (location = 0) out vec4 out_color;\n\n                void main() {\n                    vec3 color_linear = calculate_lights(v_vertex, v_normal, srgb_to_linear(color), camera_position.xyz);\n                    out_color = vec4(linear_to_srgb(color_linear), 1.0);\n                }\n            ')
        self.color = (1.0, 1.0, 1.0)

    def use(self):
        self.program['color'] = self.color

    def vertex_array(self, buffer):
        return self.ctx.vertex_array(self.program, [(buffer, '3f 3f 8x', 'in_vertex', 'in_normal')])