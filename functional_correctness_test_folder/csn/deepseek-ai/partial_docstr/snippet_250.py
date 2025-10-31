
class MHMSBFormat:

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        byte = (y // 8) * framebuf.stride + x
        offset = y % 8
        if color:
            framebuf.buf[byte] |= 1 << offset
        else:
            framebuf.buf[byte] &= ~(1 << offset)

    @staticmethod
    def get_pixel(framebuf, x, y):
        byte = (y // 8) * framebuf.stride + x
        offset = y % 8
        return (framebuf.buf[byte] >> offset) & 1

    @staticmethod
    def fill(framebuf, color):
        fill_val = 0xFF if color else 0x00
        framebuf.buf[:] = bytes([fill_val] * len(framebuf.buf))

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        for dy in range(height):
            for dx in range(width):
                MHMSBFormat.set_pixel(framebuf, x + dx, y + dy, color)
