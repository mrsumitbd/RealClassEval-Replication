
class MVLSBFormat:

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        """Set a single pixel to the given color."""
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
        """Get the color value of a single pixel."""
        index = (y >> 3) * framebuf.stride + x
        byte = framebuf.buf[index]
        mask = 1 << (y & 0x07)
        return 1 if byte & mask else 0

    @staticmethod
    def fill(framebuf, color):
        """Fill the entire framebuffer with the given color."""
        fill_value = b'\xff' if color else b'\x00'
        for i in range(len(framebuf.buf)):
            framebuf.buf[i] = ord(fill_value)

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        """Fill a rectangle with the given color."""
        for j in range(y, y + height):
            for i in range(x, x + width):
                MVLSBFormat.set_pixel(framebuf, i, j, color)
