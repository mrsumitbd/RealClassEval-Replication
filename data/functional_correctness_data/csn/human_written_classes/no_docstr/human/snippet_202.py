import moderngl
import struct
import glm

class UniformBuffer:

    def __init__(self):
        self.ctx = moderngl.get_context()
        self.data = bytearray(1024)
        self.ubo = self.ctx.buffer(self.data)

    def set_camera(self, eye, target):
        proj = glm.perspective(45.0, 1.0, 0.1, 1000.0)
        look = glm.lookAt(eye, target, (0.0, 0.0, 1.0))
        camera = proj * look
        self.data[0:64] = camera.to_bytes()

    def set_light_direction(self, x, y, z):
        self.data[64:80] = struct.pack('4f', x, y, z, 0.0)

    def use(self):
        self.ubo.write(self.data)
        self.ubo.bind_to_uniform_block()