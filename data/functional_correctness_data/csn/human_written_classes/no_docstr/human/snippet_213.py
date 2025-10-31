import struct
import moderngl
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
        self.data[64:80] = struct.pack('4f', *eye, 0.0)

    def set_light(self, light_index, position, color, power):
        offset = 80 + light_index * 48
        self.data[offset + 0:offset + 16] = struct.pack('4f', *position, 0.0)
        self.data[offset + 16:offset + 32] = struct.pack('4f', *color, 0.0)
        self.data[offset + 32:offset + 36] = struct.pack('f', power)

    def use(self):
        self.ubo.write(self.data)
        self.ubo.bind_to_uniform_block()