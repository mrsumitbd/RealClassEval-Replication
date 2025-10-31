
class MVLSBFormat:

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        if x < 0 or y < 0 or x >= framebuf.width or y >= framebuf.height:
            return
        index = (y * framebuf.width + x) // 8
        bit = (y * framebuf.width + x) % 8
        if color:
            framebuf.buf[index] |= 1 << (7 - bit)
        else:
            framebuf.buf[index] &= ~(1 << (7 - bit))

    @staticmethod
    def get_pixel(framebuf, x, y):
        if x < 0 or y < 0 or x >= framebuf.width or y >= framebuf.height:
            return 0
        index = (y * framebuf.width + x) // 8
        bit = (y * framebuf.width + x) % 8
        return (framebuf.buf[index] >> (7 - bit)) & 1

    @staticmethod
    def fill(framebuf, color):
        if color:
            framebuf.buf = bytearray([0xFF] * len(framebuf.buf))
        else:
            framebuf.buf = bytearray([0x00] * len(framebuf.buf))

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        for i in range(x, x + width):
            for j in range(y, y + height):
                MVLSBFormat.set_pixel(framebuf, i, j, color)
