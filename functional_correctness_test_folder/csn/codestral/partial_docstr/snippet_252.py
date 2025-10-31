
class RGB888Format:
    '''RGB888Format'''
    @staticmethod
    def set_pixel(framebuf, x, y, color):
        '''Set a given pixel to a color.'''
        framebuf[y * framebuf.width + x] = color

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color of a given pixel'''
        return framebuf[y * framebuf.width + x]

    @staticmethod
    def fill(framebuf, color):
        for i in range(len(framebuf)):
            framebuf[i] = color

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        for i in range(y, y + height):
            for j in range(x, x + width):
                framebuf[i * framebuf.width + j] = color
