from array import array
from PIL import Image
import moderngl

class ImageTransformer:

    def __init__(self, ctx, size, program=None):
        self.ctx = ctx
        self.size = size
        self.program = None
        self.fbo = self.ctx.framebuffer(color_attachments=[self.ctx.texture(self.size, 4)])
        if not program:
            self.program = self.ctx.program(vertex_shader='\n                    #version 330\n\n                    in vec2 in_position;\n                    in vec2 in_uv;\n                    out vec2 uv;\n\n                    void main() {\n                        gl_Position = vec4(in_position, 0.0, 1.0);\n                        uv = in_uv;\n                    }\n                ', fragment_shader='\n                    #version 330\n\n                    uniform sampler2D image;\n                    in vec2 uv;\n                    out vec4 out_color;\n\n                    void main() {\n                        // Get the Red, green, blue values from the image\n                        float red = texture(image, uv).r;\n                        // Offset green and blue\n                        float green = texture(image, uv+(1.0/20.0)).g;\n                        float blue = texture(image, uv+(2.0/20.0)).b;\n                        float alpha = texture(image, uv).a;\n                        \n                        out_color = vec4(red, green, blue, alpha);\n                    }\n                ')
        self.vertices = self.ctx.buffer(array('f', [-1, 1, 0, 1, -1, -1, 0, 0, 1, 1, 1, 1, 1, -1, 1, 0]))
        self.quad = self.ctx.vertex_array(self.program, [(self.vertices, '2f 2f', 'in_position', 'in_uv')])

    def on_render(self, texture, target=None):
        if target:
            target.use()
        else:
            self.fbo.use()
        texture.use(0)
        self.quad.render(mode=moderngl.TRIANGLE_STRIP)

    def write(self, name):
        image = Image.frombytes('RGBA', self.fbo.size, self.fbo.read(components=4))
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image.save(name, format='png')