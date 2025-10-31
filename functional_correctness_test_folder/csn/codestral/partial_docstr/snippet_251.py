
class MVLSBFormat:

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        index = (y * framebuf.width + x) // 8
        bit = (y * framebuf.width + x) % 8
        if color:
            framebuf.buffer[index] |= (1 << bit)
        else:
            framebuf.buffer[index] &= ~(1 << bit)

    @staticmethod
    def get_pixel(framebuf, x, y):
        index = (y * framebuf.width + x) // 8
        bit = (y * framebuf.width + x) % 8
        return (framebuf.buffer[index] & (1 << bit)) != 0

    @staticmethod
    def fill(framebuf, color):
        if color:
            framebuf.buffer = bytearray([0xFF] * len(framebuf.buffer))
        else:
            framebuf.buffer = bytearray([0x00] * len(framebuf.buffer))

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        for i in range(x, x + width):
            for j in range(y, y + height):
                MVLSBFormat.set_pixel(framebuf, i, j, color)
