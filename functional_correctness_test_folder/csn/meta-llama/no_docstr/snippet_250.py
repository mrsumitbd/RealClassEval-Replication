
class MHMSBFormat:

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        index = (y >> 3) * framebuf.stride + x
        byte = framebuf.buf[index]
        mask = 1 << (y & 0x07)
        if color:
            byte |= mask
        else:
            byte &= ~mask
        framebuf.buf[index] = byte

    @staticmethod
    def get_pixel(framebuf, x, y):
        index = (y >> 3) * framebuf.stride + x
        byte = framebuf.buf[index]
        mask = 1 << (y & 0x07)
        return 1 if byte & mask else 0

    @staticmethod
    def fill(framebuf, color):
        fill_value = b'\xff' if color else b'\x00'
        for i in range(len(framebuf.buf)):
            framebuf.buf[i] = ord(fill_value)

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        for j in range(y, y + height):
            for i in range(x, x + width):
                MHMSBFormat.set_pixel(framebuf, i, j, color)
