class MHMSBFormat:
    '''MHMSBFormat'''
    @staticmethod
    def set_pixel(framebuf, x, y, color):
        '''Set a given pixel to a color.'''
        w = framebuf.width
        h = framebuf.height
        if not (0 <= x < w and 0 <= y < h):
            return
        stride = (w + 7) // 8
        idx = y * stride + (x // 8)
        bit = 0x80 >> (x % 8)
        if color & 1:
            framebuf.buf[idx] |= bit
        else:
            framebuf.buf[idx] &= (~bit) & 0xFF

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color of a given pixel'''
        w = framebuf.width
        h = framebuf.height
        if not (0 <= x < w and 0 <= y < h):
            return 0
        stride = (w + 7) // 8
        idx = y * stride + (x // 8)
        bit = 0x80 >> (x % 8)
        return 1 if (framebuf.buf[idx] & bit) else 0

    @staticmethod
    def fill(framebuf, color):
        '''completely fill/clear the buffer with a color'''
        byte = 0xFF if (color & 1) else 0x00
        b = framebuf.buf
        for i in range(len(b)):
            b[i] = byte

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        '''Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior.'''
        w = framebuf.width
        h = framebuf.height
        if width <= 0 or height <= 0:
            return
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(w, x + width)
        y1 = min(h, y + height)
        if x0 >= x1 or y0 >= y1:
            return
        for yy in range(y0, y1):
            for xx in range(x0, x1):
                MHMSBFormat.set_pixel(framebuf, xx, yy, color)
