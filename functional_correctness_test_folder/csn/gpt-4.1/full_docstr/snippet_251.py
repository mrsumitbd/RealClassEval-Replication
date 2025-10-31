
class MVLSBFormat:
    '''MVLSBFormat'''

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        '''Set a given pixel to a color.'''
        width = framebuf['width']
        height = framebuf['height']
        buf = framebuf['buffer']
        if not (0 <= x < width and 0 <= y < height):
            return
        index = x + (y // 8) * width
        bit = y % 8
        if color:
            buf[index] |= (1 << bit)
        else:
            buf[index] &= ~(1 << bit)

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color of a given pixel'''
        width = framebuf['width']
        height = framebuf['height']
        buf = framebuf['buffer']
        if not (0 <= x < width and 0 <= y < height):
            return 0
        index = x + (y // 8) * width
        bit = y % 8
        return (buf[index] >> bit) & 1

    @staticmethod
    def fill(framebuf, color):
        '''completely fill/clear the buffer with a color'''
        width = framebuf['width']
        height = framebuf['height']
        buf = framebuf['buffer']
        pages = (height + 7) // 8
        value = 0xFF if color else 0x00
        for i in range(width * pages):
            buf[i] = value

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
                        MVLSBFormat.set_pixel(framebuf, i, j, color)
