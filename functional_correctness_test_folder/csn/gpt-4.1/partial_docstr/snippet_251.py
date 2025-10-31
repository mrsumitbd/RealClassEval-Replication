
class MVLSBFormat:
    @staticmethod
    def set_pixel(framebuf, x, y, color):
        width = framebuf['width']
        height = framebuf['height']
        buf = framebuf['buf']
        if not (0 <= x < width and 0 <= y < height):
            return
        index = (x // 8) + y * ((width + 7) // 8)
        bit = x % 8
        if color:
            buf[index] |= (1 << bit)
        else:
            buf[index] &= ~(1 << bit)

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color of a given pixel'''
        width = framebuf['width']
        height = framebuf['height']
        buf = framebuf['buf']
        if not (0 <= x < width and 0 <= y < height):
            return 0
        index = (x // 8) + y * ((width + 7) // 8)
        bit = x % 8
        return (buf[index] >> bit) & 1

    @staticmethod
    def fill(framebuf, color):
        width = framebuf['width']
        height = framebuf['height']
        buf = framebuf['buf']
        row_bytes = (width + 7) // 8
        fill_byte = 0xFF if color else 0x00
        for y in range(height):
            for i in range(row_bytes):
                buf[y * row_bytes + i] = fill_byte

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        fb_width = framebuf['width']
        fb_height = framebuf['height']
        for j in range(y, y + height):
            if 0 <= j < fb_height:
                for i in range(x, x + width):
                    if 0 <= i < fb_width:
                        MVLSBFormat.set_pixel(framebuf, i, j, color)
