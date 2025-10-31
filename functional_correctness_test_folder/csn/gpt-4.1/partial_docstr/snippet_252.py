
class RGB888Format:
    '''RGB888Format'''

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        '''Set a given pixel to a color.'''
        width = framebuf['width']
        height = framebuf['height']
        buf = framebuf['buffer']
        if 0 <= x < width and 0 <= y < height:
            idx = (y * width + x) * 3
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = color & 0xFF
            buf[idx] = r
            buf[idx + 1] = g
            buf[idx + 2] = b

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color of a given pixel'''
        width = framebuf['width']
        height = framebuf['height']
        buf = framebuf['buffer']
        if 0 <= x < width and 0 <= y < height:
            idx = (y * width + x) * 3
            r = buf[idx]
            g = buf[idx + 1]
            b = buf[idx + 2]
            return (r << 16) | (g << 8) | b
        return 0

    @staticmethod
    def fill(framebuf, color):
        width = framebuf['width']
        height = framebuf['height']
        buf = framebuf['buffer']
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF
        for i in range(width * height):
            idx = i * 3
            buf[idx] = r
            buf[idx + 1] = g
            buf[idx + 2] = b

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        fb_width = framebuf['width']
        fb_height = framebuf['height']
        buf = framebuf['buffer']
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF
        for j in range(y, y + height):
            if 0 <= j < fb_height:
                for i in range(x, x + width):
                    if 0 <= i < fb_width:
                        idx = (j * fb_width + i) * 3
                        buf[idx] = r
                        buf[idx + 1] = g
                        buf[idx + 2] = b
