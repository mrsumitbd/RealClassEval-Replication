
class RGB888Format:
    '''RGB888Format'''

    @staticmethod
    def _get_buf_and_size(framebuf):
        """
        Helper to obtain the underlying buffer and its dimensions.
        Supports both a raw bytearray and a FrameBuffer-like object.
        """
        # FrameBuffer-like object
        if hasattr(framebuf, 'buf') and hasattr(framebuf, 'width') and hasattr(framebuf, 'height'):
            buf = framebuf.buf
            width = framebuf.width
            height = framebuf.height
        # raw bytearray with width/height attributes
        elif hasattr(framebuf, 'width') and hasattr(framebuf, 'height'):
            buf = framebuf
            width = framebuf.width
            height = framebuf.height
        # raw bytearray only
        else:
            raise TypeError("Unsupported framebuf type")
        return buf, width, height

    @staticmethod
    def _color_to_bytes(color):
        """Convert a 24‑bit integer to a 3‑byte tuple."""
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF
        return bytes((r, g, b))

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        '''Set a given pixel to a color.'''
        buf, width, height = RGB888Format._get_buf_and_size(framebuf)
        if not (0 <= x < width and 0 <= y < height):
            return  # silently ignore out‑of‑bounds
        offset = (y * width + x) * 3
        buf[offset:offset + 3] = RGB888Format._color_to_bytes(color)

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color of a given pixel'''
        buf, width, height = RGB888Format._get_buf_and_size(framebuf)
        if not (0 <= x < width and 0 <= y < height):
            return 0  # out‑of‑bounds returns black
        offset = (y * width + x) * 3
        r, g, b = buf[offset:offset + 3]
        return (r << 16) | (g << 8) | b

    @staticmethod
    def fill(framebuf, color):
        '''completely fill/clear the buffer with a color'''
        buf, width, height = RGB888Format._get_buf_and_size(framebuf)
        pixel_bytes = RGB888Format._color_to_bytes(color)
        buf[:] = pixel_bytes * (width * height)

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        '''Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior.'''
        buf, buf_width, buf_height = RGB888Format._get_buf_and_size(framebuf)
        # Clamp rectangle to frame boundaries
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(buf_width, x + width)
        y1 = min(buf_height, y + height)
        if x0 >= x1 or y0 >= y1:
            return  # nothing to draw
        pixel_bytes = RGB888Format._color_to_bytes(color)
        for yy in range(y0, y1):
            row_start = (yy * buf_width + x0) * 3
            row_end = (yy * buf_width + x1) * 3
            buf[row_start:row_end] = pixel_bytes * (x1 - x0)
