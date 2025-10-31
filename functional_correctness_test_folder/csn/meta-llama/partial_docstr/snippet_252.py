
class RGB888Format:
    '''RGB888Format'''
    @staticmethod
    def set_pixel(framebuf, x, y, color):
        '''Set a given pixel to a color.'''
        index = (y * framebuf.stride + x) * 3
        framebuf.buf[index] = color[2]  # B
        framebuf.buf[index + 1] = color[1]  # G
        framebuf.buf[index + 2] = color[0]  # R

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color of a given pixel'''
        index = (y * framebuf.stride + x) * 3
        b = framebuf.buf[index]
        g = framebuf.buf[index + 1]
        r = framebuf.buf[index + 2]
        return (r, g, b)

    @staticmethod
    def fill(framebuf, color):
        for x in range(framebuf.width):
            for y in range(framebuf.height):
                RGB888Format.set_pixel(framebuf, x, y, color)

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        for i in range(x, min(x + width, framebuf.width)):
            for j in range(y, min(y + height, framebuf.height)):
                RGB888Format.set_pixel(framebuf, i, j, color)
