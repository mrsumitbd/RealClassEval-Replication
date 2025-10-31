
class MVLSBFormat:

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        if color:
            framebuf[y // 8] |= (1 << (x & 7))
        else:
            framebuf[y // 8] &= ~(1 << (x & 7))

    @staticmethod
    def get_pixel(framebuf, x, y):
        return (framebuf[y // 8] >> (x & 7)) & 1

    @staticmethod
    def fill(framebuf, color):
        fill_byte = 0xFF if color else 0x00
        for i in range(len(framebuf)):
            framebuf[i] = fill_byte

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        fill_byte = 0xFF if color else 0x00
        for h in range(height):
            for w in range(width):
                MVLSBFormat.set_pixel(framebuf, x + w, y + h, color)
