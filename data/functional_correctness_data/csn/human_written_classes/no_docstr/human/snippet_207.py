import moderngl

class FilmGrain:

    def __init__(self, texture):
        self.ctx = moderngl.get_context()
        self.program = self.ctx.program(vertex_shader='\n                #version 330 core\n\n                vec2 positions[3] = vec2[](\n                    vec2(-1.0, -1.0),\n                    vec2(3.0, -1.0),\n                    vec2(-1.0, 3.0)\n                );\n\n                void main() {\n                    gl_Position = vec4(positions[gl_VertexID], 0.0, 1.0);\n                }\n            ', fragment_shader='\n                #version 330 core\n                #include "hash13"\n\n                uniform sampler2D Texture;\n                uniform float time;\n\n                layout (location = 0) out vec4 out_color;\n\n                void main() {\n                    ivec2 at = ivec2(gl_FragCoord.xy);\n                    float grain = hash13(vec3(gl_FragCoord.xy, time)) * 0.5 + 0.5;\n                    out_color = texelFetch(Texture, at, 0) * grain;\n                }\n            ')
        self.sampler = self.ctx.sampler(texture=texture)
        self.vao = self.ctx.vertex_array(self.program, [])
        self.vao.vertices = 3

    def render(self, now):
        self.ctx.enable_only(self.ctx.NOTHING)
        self.sampler.use()
        self.program['time'] = now
        self.vao.render()