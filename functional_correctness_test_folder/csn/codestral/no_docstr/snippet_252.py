
class RGB888Format:

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        index = (y * framebuf.width + x) * 3
        framebuf.buf[index] = color & 0xFF
        framebuf.buf[index + 1] = (color >> 8) & 0xFF
        framebuf.buf[index + 2] = (color >> 16) & 0xFF

    @staticmethod
    def get_pixel(framebuf, x, y):
        index = (y * framebuf.width + x) * 3
        return (framebuf.buf[index + 2] << 16) | (framebuf.buf[index + 1] << 8) | framebuf.buf[index]

    @staticmethod
    def fill(framebuf, color):
        for i in range(0, len(framebuf.buf), 3):
            framebuf.buf[i] = color & 0xFF
            framebuf.buf[i + 1] = (color >> 8) & 0xFF
            framebuf.buf[i + 2] = (color >> 16) & 0xFF

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        for i in range(y, y + height):
            for j in range(x, x + width):
                RGB888Format.set_pixel(framebuf, j, i, color)
