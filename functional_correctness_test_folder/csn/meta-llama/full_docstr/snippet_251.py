
class MVLSBFormat:
    '''MVLSBFormat'''
    @staticmethod
    def set_pixel(framebuf, x, y, color):
        '''Set a given pixel to a color.'''
        index = (y >> 3) * framebuf.stride + x
        offset = y & 0x07
        if color:
            framebuf.buf[index] |= (1 << offset)
        else:
            framebuf.buf[index] &= ~(1 << offset)

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color of a given pixel'''
        index = (y >> 3) * framebuf.stride + x
        offset = y & 0x07
        return 1 if (framebuf.buf[index] & (1 << offset)) else 0

    @staticmethod
    def fill(framebuf, color):
        '''completely fill/clear the buffer with a color'''
        if color:
            framebuf.buf = bytearray([0xff] * (len(framebuf.buf)))
        else:
            framebuf.buf = bytearray([0x00] * (len(framebuf.buf)))

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        '''Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior.'''
        for j in range(y, y + height):
            for i in range(x, x + width):
                MVLSBFormat.set_pixel(framebuf, i, j, color)
