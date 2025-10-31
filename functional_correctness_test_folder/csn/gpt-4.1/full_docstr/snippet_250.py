
class MHMSBFormat:
    '''MHMSBFormat'''

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        '''Set a given pixel to a color.'''
        width = framebuf['width']
        height = framebuf['height']
        buf = framebuf['buf']
        if not (0 <= x < width and 0 <= y < height):
            return
        index = x + (y // 8) * width
        bit = y % 8
        if color:
            buf[index] |= (1 << (7 - bit))
        else:
            buf[index] &= ~(1 << (7 - bit))

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color of a given pixel'''
        width = framebuf['width']
        height = framebuf['height']
        buf = framebuf['buf']
        if not (0 <= x < width and 0 <= y < height):
            return 0
        index = x + (y // 8) * width
        bit = y % 8
        return (buf[index] >> (7 - bit)) & 1

    @staticmethod
    def fill(framebuf, color):
        '''completely fill/clear the buffer with a color'''
        buf = framebuf['buf']
        fill_byte = 0xFF if color else 0x00
        for i in range(len(buf)):
            buf[i] = fill_byte

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        '''Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior.'''
        fb_width = framebuf['width']
        fb_height = framebuf['height']
        for j in range(y, y + height):
            if 0 <= j < fb_height:
                for i in range(x, x + width):
                    if 0 <= i < fb_width:
                        MHMSBFormat.set_pixel(framebuf, i, j, color)
