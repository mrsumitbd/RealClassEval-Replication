
class RGB888Format:
    '''RGB888Format'''
    @staticmethod
    def set_pixel(framebuf, x, y, color):
        '''Set a given pixel to a color.'''
        index = (y * len(framebuf[0]) + x) * 3
        framebuf[y][x] = color

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color of a given pixel'''
        return framebuf[y][x]

    @staticmethod
    def fill(framebuf, color):
        '''Fill the entire framebuffer with the specified color.'''
        for y in range(len(framebuf)):
            for x in range(len(framebuf[0])):
                framebuf[y][x] = color

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        '''Fill a rectangle with the specified color.'''
        for dy in range(y, y + height):
            for dx in range(x, x + width):
                if 0 <= dy < len(framebuf) and 0 <= dx < len(framebuf[0]):
                    framebuf[dy][dx] = color
