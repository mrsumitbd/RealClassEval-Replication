class MVLSBFormat:
    """MVLSBFormat"""

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        """Set a given pixel to a color."""
        index = (y >> 3) * framebuf.stride + x
        offset = y & 7
        framebuf.buf[index] = framebuf.buf[index] & ~(1 << offset) | (color != 0) << offset

    @staticmethod
    def get_pixel(framebuf, x, y):
        """Get the color of a given pixel"""
        index = (y >> 3) * framebuf.stride + x
        offset = y & 7
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
        while height > 0:
            index = (y >> 3) * framebuf.stride + x
            offset = y & 7
            for w_w in range(width):
                framebuf.buf[index + w_w] = framebuf.buf[index + w_w] & ~(1 << offset) | (color != 0) << offset
            y += 1
            height -= 1