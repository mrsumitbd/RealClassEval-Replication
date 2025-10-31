
class MVLSBFormat:

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        if x < 0 or y < 0 or x >= framebuf.width or y >= framebuf.height:
            return
        index = (y * framebuf.width + x) // 8
        offset = x % 8
        mask = 1 << offset
        if color:
            framebuf.buf[index] |= mask
        else:
            framebuf.buf[index] &= ~mask

    @staticmethod
    def get_pixel(framebuf, x, y):
        if x < 0 or y < 0 or x >= framebuf.width or y >= framebuf.height:
            return 0
        index = (y * framebuf.width + x) // 8
        offset = x % 8
        mask = 1 << offset
        return 1 if framebuf.buf[index] & mask else 0

    @staticmethod
    def fill(framebuf, color):
        fill_byte = 0xFF if color else 0x00
        for i in range(len(framebuf.buf)):
            framebuf.buf[i] = fill_byte

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        for _y in range(y, y + height):
            for _x in range(x, x + width):
                MVLSBFormat.set_pixel(framebuf, _x, _y, color)
