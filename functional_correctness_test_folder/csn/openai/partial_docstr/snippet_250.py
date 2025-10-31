
class MHMSBFormat:
    @staticmethod
    def _get_buf(framebuf):
        if isinstance(framebuf, dict):
            return framebuf["buf"]
        if hasattr(framebuf, "buf"):
            return framebuf.buf
        return framebuf

    @staticmethod
    def _get_width(framebuf):
        if isinstance(framebuf, dict):
            return framebuf["width"]
        if hasattr(framebuf, "width"):
            return framebuf.width
        raise TypeError("framebuf must provide width")

    @staticmethod
    def _get_height(framebuf):
        if isinstance(framebuf, dict):
            return framebuf["height"]
        if hasattr(framebuf, "height"):
            return framebuf.height
        raise TypeError("framebuf must provide height")

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        """Set a given pixel to a color."""
        width = MHMSBFormat._get_width(framebuf)
        height = MHMSBFormat._get_height(framebuf)
        if not (0 <= x < width and 0 <= y < height):
            return
        buf = MHMSBFormat._get_buf(framebuf)
        idx = y * width + x
        byte_index = idx >> 3
        bit_index = 7 - (idx & 7)
        mask = 1 << bit_index
        if color:
            buf[byte_index] |= mask
        else:
            buf[byte_index] &= ~mask

    @staticmethod
    def get_pixel(framebuf, x, y):
        """Return the pixel value (0 or 1)."""
        width = MHMSBFormat._get_width(framebuf)
        height = MHMSBFormat._get_height(framebuf)
        if not (0 <= x < width and 0 <= y < height):
            return 0
        buf = MHMSBFormat._get_buf(framebuf)
        idx = y * width + x
        byte_index = idx >> 3
        bit_index = 7 - (idx & 7)
        return (buf[byte_index] >> bit_index) & 1

    @staticmethod
    def fill(framebuf, color):
        """completely fill/clear the buffer with a color"""
        buf = MHMSBFormat._get_buf(framebuf)
        value = 0xFF if color else 0x00
        for i in range(len(buf)):
            buf[i] = value

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        """Draw a rectangle at the given location, size and color.
        The ``fill_rect`` method draws both the outline and interior."""
        w = MHMSBFormat._get_width(framebuf)
        h = MHMSBFormat._get_height(framebuf)
        for yy in range(y, y + height):
            if yy < 0 or yy >= h:
                continue
            for xx in range(x, x + width):
                if xx < 0 or xx >= w:
                    continue
                MHMSBFormat.set_pixel(framebuf, xx, yy, color)
