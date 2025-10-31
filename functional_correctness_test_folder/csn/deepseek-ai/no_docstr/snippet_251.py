
class MVLSBFormat:

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        index = (y // 8) * framebuf.stride + x
        offset = y % 8
        if color:
            framebuf.buf[index] |= (1 << offset)
        else:
            framebuf.buf[index] &= ~(1 << offset)

    @staticmethod
    def get_pixel(framebuf, x, y):
        index = (y // 8) * framebuf.stride + x
        offset = y % 8
        return (framebuf.buf[index] >> offset) & 1

    @staticmethod
    def fill(framebuf, color):
        fill_val = 0xFF if color else 0x00
        framebuf.buf[:] = bytes([fill_val] * len(framebuf.buf))

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        for dy in range(height):
            for dx in range(width):
                MVLSBFormat.set_pixel(framebuf, x + dx, y + dy, color)
