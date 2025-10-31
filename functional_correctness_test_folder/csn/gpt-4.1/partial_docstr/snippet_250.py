
class MHMSBFormat:

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
            buf[index] |= (1 << bit)
        else:
            buf[index] &= ~(1 << bit)

    @staticmethod
    def get_pixel(framebuf, x, y):
        width = framebuf['width']
        height = framebuf['height']
        buf = framebuf['buf']
        if not (0 <= x < width and 0 <= y < height):
            return 0
        index = x + (y // 8) * width
        bit = y % 8
        return 1 if (buf[index] & (1 << bit)) else 0

    @staticmethod
    def fill(framebuf, color):
        '''completely fill/clear the buffer with a color'''
        width = framebuf['width']
        height = framebuf['height']
        buf = framebuf['buf']
        pages = (height + 7) // 8
        val = 0xFF if color else 0x00
        for page in range(pages):
            for x in range(width):
                buf[x + page * width] = val

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        '''Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior.'''
        fb_width = framebuf['width']
        fb_height = framebuf['height']
        for dy in range(height):
            yy = y + dy
            if 0 <= yy < fb_height:
                for dx in range(width):
                    xx = x + dx
                    if 0 <= xx < fb_width:
                        MHMSBFormat.set_pixel(framebuf, xx, yy, color)
