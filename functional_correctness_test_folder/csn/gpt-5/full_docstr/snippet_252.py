class RGB888Format:
    '''RGB888Format'''

    @staticmethod
    def _get_buf_wh_stride(framebuf):
        buf = getattr(framebuf, 'buffer', None)
        if buf is None:
            buf = getattr(framebuf, 'buf', None)
        if buf is None:
            raise AttributeError('framebuf must have buffer or buf attribute')
        w = getattr(framebuf, 'width', None)
        h = getattr(framebuf, 'height', None)
        if w is None or h is None:
            raise AttributeError(
                'framebuf must have width and height attributes')
        stride = getattr(framebuf, 'stride', None)
        if stride is None:
            stride = w * 3
        return buf, w, h, stride

    @staticmethod
    def _color_to_bytes(color):
        if isinstance(color, (tuple, list)) and len(color) == 3:
            r, g, b = color
            r &= 0xFF
            g &= 0xFF
            b &= 0xFF
        else:
            c = int(color) & 0xFFFFFF
            r = (c >> 16) & 0xFF
            g = (c >> 8) & 0xFF
            b = c & 0xFF
        return r, g, b

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        '''Set a given pixel to a color.'''
        buf, w, h, stride = RGB888Format._get_buf_wh_stride(framebuf)
        if not (0 <= x < w and 0 <= y < h):
            return
        r, g, b = RGB888Format._color_to_bytes(color)
        idx = y * stride + x * 3
        buf[idx] = r
        buf[idx + 1] = g
        buf[idx + 2] = b

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color of a given pixel'''
        buf, w, h, stride = RGB888Format._get_buf_wh_stride(framebuf)
        if not (0 <= x < w and 0 <= y < h):
            return 0
        idx = y * stride + x * 3
        r = buf[idx]
        g = buf[idx + 1]
        b = buf[idx + 2]
        return (r << 16) | (g << 8) | b

    @staticmethod
    def fill(framebuf, color):
        '''completely fill/clear the buffer with a color'''
        buf, w, h, stride = RGB888Format._get_buf_wh_stride(framebuf)
        r, g, b = RGB888Format._color_to_bytes(color)
        row_pattern = bytes((r, g, b)) * w
        for y in range(h):
            start = y * stride
            end = start + w * 3
            buf[start:end] = row_pattern

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        '''Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior.'''
        buf, w, h, stride = RGB888Format._get_buf_wh_stride(framebuf)
        if width <= 0 or height <= 0:
            return
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(w, x + width)
        y1 = min(h, y + height)
        if x0 >= x1 or y0 >= y1:
            return
        r, g, b = RGB888Format._color_to_bytes(color)
        row_pattern = bytes((r, g, b)) * (x1 - x0)
        for row in range(y0, y1):
            start = row * stride + x0 * 3
            end = start + (x1 - x0) * 3
            buf[start:end] = row_pattern
