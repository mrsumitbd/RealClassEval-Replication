
class RGB888Format:
    '''RGB888Format'''
    @staticmethod
    def set_pixel(framebuf, x, y, color):
        '''Set a given pixel to a color.'''
        index = (y * framebuf.stride + x) * 3
        framebuf.buf[index] = color[2]  # Blue
        framebuf.buf[index + 1] = color[1]  # Green
        framebuf.buf[index + 2] = color[0]  # Red

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color of a given pixel'''
        index = (y * framebuf.stride + x) * 3
        return (framebuf.buf[index + 2], framebuf.buf[index + 1], framebuf.buf[index])

    @staticmethod
    def fill(framebuf, color):
        '''completely fill/clear the buffer with a color'''
        for i in range(0, len(framebuf.buf), 3):
            framebuf.buf[i] = color[2]  # Blue
            framebuf.buf[i + 1] = color[1]  # Green
            framebuf.buf[i + 2] = color[0]  # Red

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        '''Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior.'''
        for j in range(y, y + height):
            for i in range(x, x + width):
                RGB888Format.set_pixel(framebuf, i, j, color)
