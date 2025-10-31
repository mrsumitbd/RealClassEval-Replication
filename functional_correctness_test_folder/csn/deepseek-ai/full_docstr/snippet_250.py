
class MHMSBFormat:
    '''MHMSBFormat'''
    @staticmethod
    def set_pixel(framebuf, x, y, color):
        '''Set a given pixel to a color.'''
        index = (y // 8) * framebuf.width + x
        offset = y % 8
        if color:
            framebuf.buf[index] |= 1 << offset
        else:
            framebuf.buf[index] &= ~(1 << offset)

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color of a given pixel'''
        index = (y // 8) * framebuf.width + x
        offset = y % 8
        return (framebuf.buf[index] >> offset) & 1

    @staticmethod
    def fill(framebuf, color):
        '''completely fill/clear the buffer with a color'''
        fill_value = 0xFF if color else 0x00
        for i in range(len(framebuf.buf)):
            framebuf.buf[i] = fill_value

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        '''Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior.'''
        for dy in range(height):
            for dx in range(width):
                MHMSBFormat.set_pixel(framebuf, x + dx, y + dy, color)
