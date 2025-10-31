
class RGB888Format:
    '''RGB888Format'''
    @staticmethod
    def set_pixel(framebuf, x, y, color):
        '''Set a given pixel to a color.'''
        index = (y * framebuf.width + x) * 3
        framebuf.buf[index:index+3] = color.to_bytes(3, 'big')

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color of a given pixel'''
        index = (y * framebuf.width + x) * 3
        return int.from_bytes(framebuf.buf[index:index+3], 'big')

    @staticmethod
    def fill(framebuf, color):
        framebuf.buf[:] = color.to_bytes(
            3, 'big') * (framebuf.width * framebuf.height)

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        color_bytes = color.to_bytes(3, 'big')
        for _y in range(y, y + height):
            index = (_y * framebuf.width + x) * 3
            framebuf.buf[index:index + width * 3] = color_bytes * width
