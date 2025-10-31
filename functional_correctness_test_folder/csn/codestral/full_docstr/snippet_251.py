
class MVLSBFormat:
    '''MVLSBFormat'''
    @staticmethod
    def set_pixel(framebuf, x, y, color):
        '''Set a given pixel to a color.'''
        index = y * framebuf.width + x
        framebuf.buf[index] = color

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color of a given pixel'''
        index = y * framebuf.width + x
        return framebuf.buf[index]

    @staticmethod
    def fill(framebuf, color):
        '''completely fill/clear the buffer with a color'''
        framebuf.buf = [color] * (framebuf.width * framebuf.height)

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        '''Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior.'''
        for i in range(x, x + width):
            for j in range(y, y + height):
                MVLSBFormat.set_pixel(framebuf, i, j, color)
