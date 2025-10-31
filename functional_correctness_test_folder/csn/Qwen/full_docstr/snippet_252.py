
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
        '''completely fill/clear the buffer with a color'''
        framebuf.buf[:] = color.to_bytes(
            3, 'big') * (framebuf.width * framebuf.height)

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        '''Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior.'''
        for _y in range(y, y + height):
            for _x in range(x, x + width):
                RGB888Format.set_pixel(framebuf, _x, _y, color)
