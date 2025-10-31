class RGB888Format:
    """RGB888Format"""

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        """Set a given pixel to a color."""
        index = (y * framebuf.stride + x) * 3
        if isinstance(color, tuple):
            framebuf.buf[index:index + 3] = bytes(color)
        else:
            framebuf.buf[index:index + 3] = bytes((color >> 16 & 255, color >> 8 & 255, color & 255))

    @staticmethod
    def get_pixel(framebuf, x, y):
        """Get the color of a given pixel"""
        index = (y * framebuf.stride + x) * 3
        return framebuf.buf[index] << 16 | framebuf.buf[index + 1] << 8 | framebuf.buf[index + 2]

    @staticmethod
    def fill(framebuf, color):
        """completely fill/clear the buffer with a color"""
        fill = (color >> 16 & 255, color >> 8 & 255, color & 255)
        for i in range(0, len(framebuf.buf), 3):
            framebuf.buf[i:i + 3] = bytes(fill)

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        """Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior."""
        fill = (color >> 16 & 255, color >> 8 & 255, color & 255)
        for _x in range(x, x + width):
            for _y in range(y, y + height):
                index = (_y * framebuf.stride + _x) * 3
                framebuf.buf[index:index + 3] = bytes(fill)