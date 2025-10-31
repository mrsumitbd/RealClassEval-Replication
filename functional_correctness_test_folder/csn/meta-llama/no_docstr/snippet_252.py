
class RGB888Format:

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        index = (y * framebuf.stride + x) * 3
        framebuf.buf[index] = color[2]
        framebuf.buf[index + 1] = color[1]
        framebuf.buf[index + 2] = color[0]

    @staticmethod
    def get_pixel(framebuf, x, y):
        index = (y * framebuf.stride + x) * 3
        return (framebuf.buf[index + 2], framebuf.buf[index + 1], framebuf.buf[index])

    @staticmethod
    def fill(framebuf, color):
        for y in range(framebuf.height):
            for x in range(framebuf.width):
                RGB888Format.set_pixel(framebuf, x, y, color)

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        for j in range(y, min(y + height, framebuf.height)):
            for i in range(x, min(x + width, framebuf.width)):
                RGB888Format.set_pixel(framebuf, i, j, color)
