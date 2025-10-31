class RGB888Format:
    @staticmethod
    def _get_attrs(framebuf):
        buf = getattr(framebuf, "buffer", None)
        if buf is None:
            buf = framebuf
        width = getattr(framebuf, "width", None)
        height = getattr(framebuf, "height", None)
        if width is None or height is None:
            raise AttributeError("framebuf must provide width and height")
        stride = getattr(framebuf, "stride", width * 3)
        return buf, width, height, stride

    @staticmethod
    def _color_bytes(color):
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF
        return bytes((r, g, b))

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        buf, width, height, stride = RGB888Format._get_attrs(framebuf)
        if not (0 <= x < width and 0 <= y < height):
            return
        off = y * stride + x * 3
        c = RGB888Format._color_bytes(color)
        buf[off:off + 3] = c

    @staticmethod
    def get_pixel(framebuf, x, y):
        buf, width, height, stride = RGB888Format._get_attrs(framebuf)
        if not (0 <= x < width and 0 <= y < height):
            return 0
        off = y * stride + x * 3
        r, g, b = buf[off], buf[off + 1], buf[off + 2]
        return (r << 16) | (g << 8) | b

    @staticmethod
    def fill(framebuf, color):
        buf, width, height, stride = RGB888Format._get_attrs(framebuf)
        if width <= 0 or height <= 0:
            return
        c = RGB888Format._color_bytes(color)
        row = (c * width)
        for y in range(height):
            start = y * stride
            end = start + width * 3
            buf[start:end] = row

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        buf, fbw, fbh, stride = RGB888Format._get_attrs(framebuf)
        if width <= 0 or height <= 0:
            return
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(fbw, x + width)
        y1 = min(fbh, y + height)
        if x0 >= x1 or y0 >= y1:
            return
        w = x1 - x0
        c = RGB888Format._color_bytes(color)
        row = (c * w)
        for yy in range(y0, y1):
            start = yy * stride + x0 * 3
            end = start + w * 3
            buf[start:end] = row
