class MVLSBFormat:

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        """Set the pixel at (x, y) to the given color."""
        framebuf[y][x] = color

    @staticmethod
    def get_pixel(framebuf, x, y):
        """Get the color of a given pixel."""
        return framebuf[y][x]

    @staticmethod
    def fill(framebuf, color):
        """Fill the entire frame buffer with the given color."""
        for row in framebuf:
            for i in range(len(row)):
                row[i] = color

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        """Fill a rectangle area with the given color."""
        for row in range(y, y + height):
            for col in range(x, x + width):
                framebuf[row][col] = color
