class MHMSBFormat:
    """MHMSBFormat"""

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        """Set a given pixel to a color."""
        index = (y * framebuf.stride + x) // 8
        offset = 7 - x & 7
        framebuf.buf[index] = framebuf.buf[index] & ~(1 << offset) | (color != 0) << offset

    @staticmethod
    def get_pixel(framebuf, x, y):
        """Get the color of a given pixel"""
        index = (y * framebuf.stride + x) // 8
        offset = 7 - x & 7
        return framebuf.buf[index] >> offset & 1

    @staticmethod
    def fill(framebuf, color):
        """completely fill/clear the buffer with a color"""
        if color:
            fill = 255
        else:
            fill = 0
        for i in range(len(framebuf.buf)):
            framebuf.buf[i] = fill

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        """Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior."""
        for _x in range(x, x + width):
            offset = 7 - _x & 7
            for _y in range(y, y + height):
                index = (_y * framebuf.stride + _x) // 8
                framebuf.buf[index] = framebuf.buf[index] & ~(1 << offset) | (color != 0) << offset