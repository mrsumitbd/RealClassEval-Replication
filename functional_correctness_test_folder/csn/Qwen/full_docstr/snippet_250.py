
class MHMSBFormat:
    '''MHMSBFormat'''
    @staticmethod
    def set_pixel(framebuf, x, y, color):
        '''Set a given pixel to a color.'''
        framebuf[x + (y * framebuf.width)] = color

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color of a given pixel'''
        return framebuf[x + (y * framebuf.width)]

    @staticmethod
    def fill(framebuf, color):
        '''completely fill/clear the buffer with a color'''
        for i in range(len(framebuf)):
            framebuf[i] = color

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        '''Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior.'''
        for _y in range(y, y + height):
            for _x in range(x, x + width):
                MHMSBFormat.set_pixel(framebuf, _x, _y, color)
