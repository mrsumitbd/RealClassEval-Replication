
class MHMSBFormat:

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        index = (y * framebuf.width + x) // 8
        mask = 0x80 >> (x % 8)
        if color:
            framebuf.buf[index] |= mask
        else:
            framebuf.buf[index] &= ~mask

    @staticmethod
    def get_pixel(framebuf, x, y):
        index = (y * framebuf.width + x) // 8
        mask = 0x80 >> (x % 8)
        return 1 if framebuf.buf[index] & mask else 0

    @staticmethod
    def fill(framebuf, color):
        fill_byte = 0xFF if color else 0x00
        for i in range(len(framebuf.buf)):
            framebuf.buf[i] = fill_byte

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        fill_byte = 0xFF if color else 0x00
        for _y in range(y, y + height):
            for _x in range(x, x + width):
                MHMSBFormat.set_pixel(framebuf, _x, _y, color)
