
class MHMSBFormat:
    '''MHMSBFormat'''
    @staticmethod
    def set_pixel(framebuf, x, y, color):
        '''Set a given pixel to a color.'''
        framebuf.pixel(x, y, color)

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color of a given pixel'''
        return framebuf.pixel(x, y)

    @staticmethod
    def fill(framebuf, color):
        '''completely fill/clear the buffer with a color'''
        framebuf.fill(color)

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        '''Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior.'''
        framebuf.fill_rect(x, y, width, height, color)
