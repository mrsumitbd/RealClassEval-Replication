
class MHMSBFormat:

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        '''Set a given pixel to a color.'''
        if 0 <= x < framebuf.width and 0 <= y < framebuf.height:
            index = (y * framebuf.width + x) // 8
            shift = 7 - (x % 8)
            mask = 1 << shift
            if color:
                framebuf.buf[index] |= mask
            else:
                framebuf.buf[index] &= ~mask

    @staticmethod
    def get_pixel(framebuf, x, y):
        if 0 <= x < framebuf.width and 0 <= y < framebuf.height:
            index = (y * framebuf.width + x) // 8
            shift = 7 - (x % 8)
            mask = 1 << shift
            return 1 if framebuf.buf[index] & mask else 0
        return 0

    @staticmethod
    def fill(framebuf, color):
        '''completely fill/clear the buffer with a color'''
        fill_byte = 0xFF if color else 0x00
        for i in range(len(framebuf.buf)):
            framebuf.buf[i] = fill_byte

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        '''Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior.'''
        for _y in range(y, y + height):
            for _x in range(x, x + width):
                MHMSBFormat.set_pixel(framebuf, _x, _y, color)
