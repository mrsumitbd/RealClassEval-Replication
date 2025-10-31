
class MHMSBFormat:

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        index = (y // 8) * framebuf.width + x
        offset = y % 8
        if color:
            framebuf.buffer[index] |= (1 << offset)
        else:
            framebuf.buffer[index] &= ~(1 << offset)

    @staticmethod
    def get_pixel(framebuf, x, y):
        index = (y // 8) * framebuf.width + x
        offset = y % 8
        return (framebuf.buffer[index] >> offset) & 1

    @staticmethod
    def fill(framebuf, color):
        fill_val = 0xFF if color else 0x00
        framebuf.buffer = bytearray([fill_val] * len(framebuf.buffer))

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        for dy in range(height):
            for dx in range(width):
                MHMSBFormat.set_pixel(framebuf, x + dx, y + dy, color)
