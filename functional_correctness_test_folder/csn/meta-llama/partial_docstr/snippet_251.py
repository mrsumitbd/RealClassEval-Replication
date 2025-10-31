
class MVLSBFormat:

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        index = (y * framebuf.stride + x) // 8
        offset = x & 0x07
        mask = 1 << offset
        if color:
            framebuf.buf[index] |= mask
        else:
            framebuf.buf[index] &= ~mask

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color of a given pixel'''
        index = (y * framebuf.stride + x) // 8
        offset = x & 0x07
        mask = 1 << offset
        return 1 if (framebuf.buf[index] & mask) else 0

    @staticmethod
    def fill(framebuf, color):
        if color:
            framebuf.buf[:] = b'\xff' * len(framebuf.buf)
        else:
            framebuf.buf[:] = b'\x00' * len(framebuf.buf)

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        for j in range(y, y + height):
            for i in range(x, x + width):
                MVLSBFormat.set_pixel(framebuf, i, j, color)
