import zengl_playground
import moderngl

class Example:

    def __init__(self):
        self.ctx = moderngl.get_context()
        app = zengl_playground.get_app()
        app.setup_moderngl(self.ctx)
        self.program = self.ctx.program(vertex_shader='\n                #version 330 core\n\n                #include "main_uniform_buffer"\n\n                uniform vec3 position;\n                uniform float scale;\n\n                layout (location = 0) in vec3 in_vertex;\n                layout (location = 1) in vec3 in_normal;\n                layout (location = 2) in vec2 in_uv;\n\n                out vec3 v_vertex;\n                out vec3 v_normal;\n                out vec2 v_uv;\n\n                void main() {\n                    v_vertex = position + in_vertex * scale;\n                    v_normal = in_normal;\n                    v_uv = in_uv;\n\n                    gl_Position = camera_matrix * vec4(v_vertex, 1.0);\n                }\n            ', fragment_shader='\n                #version 330 core\n\n                uniform sampler2D Texture;\n                uniform bool use_texture;\n                uniform vec3 color;\n\n                in vec3 v_vertex;\n                in vec3 v_normal;\n                in vec2 v_uv;\n\n                layout (location = 0) out vec4 out_color;\n\n                void main() {\n                    out_color = vec4(color, 1.0);\n                    if (use_texture) {\n                        out_color *= texture(Texture, v_uv);\n                    }\n                }\n            ')
        self.texture = ImageTexture('examples/data/textures/crate.png')
        self.car_geometry = ModelGeometry('examples/data/models/lowpoly_toy_car.obj')
        self.car = Mesh(self.program, self.car_geometry)
        self.crate_geometry = ModelGeometry('examples/data/models/crate.obj')
        self.crate = Mesh(self.program, self.crate_geometry, self.texture)

    def render(self):
        self.ctx.screen.use()
        self.ctx.enable(self.ctx.DEPTH_TEST)
        self.car.render((-0.4, 0.0, 0.0), (1.0, 0.0, 0.0), 0.2)
        self.crate.render((0.0, 0.0, 0.0), (1.0, 1.0, 1.0), 0.2)
        self.car.render((0.4, 0.0, 0.0), (0.0, 0.0, 1.0), 0.2)