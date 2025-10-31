class RGB888Format:
    '''RGB888Format'''

    @staticmethod
    def _resolve_framebuf(framebuf):
        # Extract buffer, width, height, and stride (bytes per row)
        buf = None
        width = None
        height = None
        stride = None

        # Object with attributes
        if hasattr(framebuf, 'buffer'):
            buf = framebuf.buffer
        elif hasattr(framebuf, 'buf'):
            buf = framebuf.buf
        elif hasattr(framebuf, 'data'):
            buf = framebuf.data
        elif isinstance(framebuf, (bytearray, bytes, memoryview)):
            # Only buffer provided; width/height/stride must be in attributes or elsewhere
            buf = framebuf

        if hasattr(framebuf, 'width'):
            width = framebuf.width
        if hasattr(framebuf, 'height'):
            height = framebuf.height
        if hasattr(framebuf, 'stride'):
            stride = framebuf.stride
        elif hasattr(framebuf, 'pitch'):
            stride = framebuf.pitch
        elif hasattr(framebuf, 'row_bytes'):
            stride = framebuf.row_bytes

        # Mapping-like
        if buf is None and isinstance(framebuf, dict):
            buf = framebuf.get('buffer') or framebuf.get(
                'buf') or framebuf.get('data')
            width = framebuf.get('width', width)
            height = framebuf.get('height', height)
            stride = framebuf.get('stride', stride) or framebuf.get(
                'pitch', stride) or framebuf.get('row_bytes', stride)

        # Tuple/list forms: (buf, width, height[, stride])
        if buf is None and isinstance(framebuf, (tuple, list)) and len(framebuf) >= 3:
            buf = framebuf[0]
            width = framebuf[1]
            height = framebuf[2]
            if len(framebuf) >= 4:
                stride = framebuf[3]

        if buf is None or width is None or height is None:
            raise ValueError("framebuf must provide buffer, width, and height")

        # Ensure buffer is mutable; allow memoryview of bytes if writable later
        mv = memoryview(buf)
        if not mv.contiguous:
            mv = mv.cast('B')

        # Default stride if not provided
        if stride is None:
            stride = int(width) * 3

        return mv, int(width), int(height), int(stride)

    @staticmethod
    def _color_to_rgb(color):
        # Accept int 0xRRGGBB or (r,g,b)
        if isinstance(color, int):
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = color & 0xFF
            return r, g, b
        if isinstance(color, (tuple, list)) and len(color) == 3:
            r, g, b = color
            return int(r) & 0xFF, int(g) & 0xFF, int(b) & 0xFF
        raise ValueError("color must be int 0xRRGGBB or (r, g, b)")

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        '''Set a given pixel to a color.'''
        buf, width, height, stride = RGB888Format._resolve_framebuf(framebuf)
        xi = int(x)
        yi = int(y)
        if xi < 0 or yi < 0 or xi >= width or yi >= height:
            return
        r, g, b = RGB888Format._color_to_rgb(color)
        idx = yi * stride + xi * 3
        # Ensure writable view
        if buf.readonly:
            raise TypeError("frame buffer is read-only")
        buf[idx] = r
        buf[idx + 1] = g
        buf[idx + 2] = b

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color of a given pixel'''
        buf, width, height, stride = RGB888Format._resolve_framebuf(framebuf)
        xi = int(x)
        yi = int(y)
        if xi < 0 or yi < 0 or xi >= width or yi >= height:
            return 0
        idx = yi * stride + xi * 3
        r = buf[idx]
        g = buf[idx + 1]
        b = buf[idx + 2]
        return (r << 16) | (g << 8) | b

    @staticmethod
    def fill(framebuf, color):
        buf, width, height, stride = RGB888Format._resolve_framebuf(framebuf)
        if buf.readonly:
            raise TypeError("frame buffer is read-only")
        r, g, b = RGB888Format._color_to_rgb(color)
        # Build one row worth of pixel data for the active width
        row_active = bytes([r, g, b]) * width
        for y in range(height):
            base = y * stride
            buf[base:base + width * 3] = row_active

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        buf, fbw, fbh, stride = RGB888Format._resolve_framebuf(framebuf)
        if buf.readonly:
            raise TypeError("frame buffer is read-only")

        x0 = int(x)
        y0 = int(y)
        w = int(width)
        h = int(height)

        if w <= 0 or h <= 0:
            return

        # Clamp rectangle to framebuffer bounds
        if x0 < 0:
            w += x0
            x0 = 0
        if y0 < 0:
            h += y0
            y0 = 0
        if x0 >= fbw or y0 >= fbh:
            return
        if x0 + w > fbw:
            w = fbw - x0
        if y0 + h > fbh:
            h = fbh - y0
        if w <= 0 or h <= 0:
            return

        r, g, b = RGB888Format._color_to_rgb(color)
        row_fill = bytes([r, g, b]) * w

        for yy in range(y0, y0 + h):
            start = yy * stride + x0 * 3
            buf[start:start + w * 3] = row_fill
