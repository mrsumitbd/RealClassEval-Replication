from PIL import Image, ImageDraw, ImageFont
import moderngl
import pygame

class Overlay:

    def __init__(self, size):
        self.ctx = moderngl.get_context()
        self.img = Image.new('RGBA', size)
        self.draw = ImageDraw.Draw(self.img)
        self.draw.font = ImageFont.truetype('examples/data/fonts/OpenSans/OpenSans-Medium.ttf', 20)
        self.texture = self.ctx.texture(size, 4)
        self.program = self.ctx.program(vertex_shader='\n                #version 330 core\n\n                vec2 positions[3] = vec2[](\n                    vec2(-1.0, -1.0),\n                    vec2(3.0, -1.0),\n                    vec2(-1.0, 3.0)\n                );\n\n                void main() {\n                    gl_Position = vec4(positions[gl_VertexID], 0.0, 1.0);\n                }\n            ', fragment_shader='\n                #version 330 core\n\n                uniform sampler2D Texture;\n\n                layout (location = 0) out vec4 out_color;\n\n                void main() {\n                    ivec2 at = ivec2(gl_FragCoord.xy);\n                    at.y = textureSize(Texture, 0).y - at.y - 1;\n                    out_color = texelFetch(Texture, at, 0);\n                }\n            ')
        self.sampler = self.ctx.sampler(texture=self.texture)
        self.vao = self.ctx.vertex_array(self.program, [])
        self.vao.vertices = 3
        self.clock = pygame.time.Clock()
        self.fps = 0.0

    def render(self):
        self.clock.tick()
        mouse = pygame.mouse.get_pos()
        now = pygame.time.get_ticks() / 1000.0
        self.fps = self.fps * 0.95 + self.clock.get_fps() * 0.05
        self.draw.rectangle((0, 0, *self.img.size), fill=(0, 0, 0, 0))
        self.draw.text((100, 100), f'fps: {self.fps:.2f}', fill='#fff')
        self.draw.text((100, 130), f'elapsed: {now:.2f}s', fill='#f00')
        self.draw.text((100, 160), f'mouse: {mouse}', fill='#fff')
        rect = self.draw.textbbox((0, 0), 'Hello, World!')
        pos = (mouse[0] - (rect[0] + rect[2]) / 2, mouse[1] - 40)
        self.draw.text(pos, 'Hello, World!', fill='#fff')
        self.texture.write(self.img.tobytes())
        self.ctx.enable_only(self.ctx.BLEND)
        self.sampler.use()
        self.vao.render()