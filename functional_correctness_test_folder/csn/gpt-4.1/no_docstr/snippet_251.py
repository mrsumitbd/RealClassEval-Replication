
class MVLSBFormat:

    @staticmethod
    def set_pixel(framebuf, x, y, color):
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
        return (buf[index] >> bit) & 1

    @staticmethod
    def fill(framebuf, color):
        width = framebuf['width']
        height = framebuf['height']
        buf = framebuf['buf']
        rows = (height + 7) // 8
        fill_byte = 0xFF if color else 0x00
        for i in range(width * rows):
            buf[i] = fill_byte

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        fb_width = framebuf['width']
        fb_height = framebuf['height']
        buf = framebuf['buf']
        for iy in range(y, y + height):
            if 0 <= iy < fb_height:
                for ix in range(x, x + width):
                    if 0 <= ix < fb_width:
                        MVLSBFormat.set_pixel(framebuf, ix, iy, color)
