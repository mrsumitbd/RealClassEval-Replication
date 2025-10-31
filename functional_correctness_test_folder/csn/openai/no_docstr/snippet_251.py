
class MVLSBFormat:
    @staticmethod
    def set_pixel(framebuf, x, y, color):
        """
        Set a pixel in a 4‑bit per pixel buffer stored as a list of bytearrays.
        Each byte contains two pixels: lower nibble is pixel 0, upper nibble is pixel 1.
        """
        color &= 0x0F  # keep only 4 bits
        byte_index = x // 2
        nibble = x % 2
        if nibble == 0:
            # lower nibble
            framebuf[y][byte_index] = (framebuf[y][byte_index] & 0xF0) | color
        else:
            # upper nibble
            framebuf[y][byte_index] = (
                framebuf[y][byte_index] & 0x0F) | (color << 4)

    @staticmethod
    def get_pixel(framebuf, x, y):
        """
        Retrieve a pixel value from the buffer.
        """
        byte_index = x // 2
        nibble = x % 2
        byte = framebuf[y][byte_index]
        if nibble == 0:
            return byte & 0x0F
        else:
            return (byte >> 4) & 0x0F

    @staticmethod
    def fill(framebuf, color):
        """
        Fill the entire buffer with the given color.
        """
        color &= 0x0F
        packed = (color << 4) | color
        for row in framebuf:
            for i in range(len(row)):
                row[i] = packed

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        """
        Fill a rectangle area with the given color.
        """
        color &= 0x0F
        packed = (color << 4) | color
        for row_index in range(y, y + height):
            row = framebuf[row_index]
            for col_index in range(x, x + width):
                byte_index = col_index // 2
                nibble = col_index % 2
                if nibble == 0:
                    row[byte_index] = (row[byte_index] & 0xF0) | color
                else:
                    row[byte_index] = (row[byte_index] & 0x0F) | (color << 4)
