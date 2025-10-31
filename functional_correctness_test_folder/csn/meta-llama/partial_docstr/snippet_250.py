
class MHMSBFormat:

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        '''Set a given pixel to a color.'''
        index = (y * framebuf.stride + x) // 8
        mask = 1 << (7 - (x & 7))
        if color:
            framebuf.buf[index] |= mask
        else:
            framebuf.buf[index] &= ~mask

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color value of a given pixel.'''
        index = (y * framebuf.stride + x) // 8
        mask = 1 << (7 - (x & 7))
        return 1 if framebuf.buf[index] & mask else 0

    @staticmethod
    def fill(framebuf, color):
        '''completely fill/clear the buffer with a color'''
        if color:
            framebuf.buf = bytearray([0xff] * len(framebuf.buf))
        else:
            framebuf.buf = bytearray([0x00] * len(framebuf.buf))

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        '''Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior.'''
        for i in range(y, y + height):
            for j in range(x, x + width):
                MHMSBFormat.set_pixel(framebuf, j, i, color)
