class MVLSBFormat:

    @staticmethod
    def _get_buffer(framebuf):
        if hasattr(framebuf, 'buffer'):
            return framebuf.buffer
        if hasattr(framebuf, 'buf'):
            return framebuf.buf
        if hasattr(framebuf, 'data'):
            return framebuf.data
        if isinstance(framebuf, (bytearray, memoryview)):
            return framebuf
        raise AttributeError(
            "Frame buffer object must provide a 'buffer' (or 'buf'/'data').")

    @staticmethod
    def _get_width(framebuf):
        if hasattr(framebuf, 'width'):
            return framebuf.width
        raise AttributeError("Frame buffer object must provide 'width'.")

    @staticmethod
    def _get_height(framebuf):
        if hasattr(framebuf, 'height'):
            return framebuf.height
        raise AttributeError("Frame buffer object must provide 'height'.")

    @staticmethod
    def _get_stride(framebuf, width):
        # Stride is bytes per 8-pixel vertical band. For MONO_VLSB it's typically equal to width.
        return getattr(framebuf, 'stride', width)

    @staticmethod
    def _index_and_mask(x, y, stride):
        byte_index = x + (y >> 3) * stride
        bit_mask = 1 << (y & 7)
        return byte_index, bit_mask

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        buf = MVLSBFormat._get_buffer(framebuf)
        width = MVLSBFormat._get_width(framebuf)
        height = MVLSBFormat._get_height(framebuf)
        if x < 0 or y < 0 or x >= width or y >= height:
            return
        stride = MVLSBFormat._get_stride(framebuf, width)
        idx, mask = MVLSBFormat._index_and_mask(x, y, stride)
        if color:
            buf[idx] = buf[idx] | mask
        else:
            buf[idx] = buf[idx] & (~mask & 0xFF)

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color of a given pixel'''
        buf = MVLSBFormat._get_buffer(framebuf)
        width = MVLSBFormat._get_width(framebuf)
        height = MVLSBFormat._get_height(framebuf)
        if x < 0 or y < 0 or x >= width or y >= height:
            return 0
        stride = MVLSBFormat._get_stride(framebuf, width)
        idx, mask = MVLSBFormat._index_and_mask(x, y, stride)
        return 1 if (buf[idx] & mask) else 0

    @staticmethod
    def fill(framebuf, color):
        buf = MVLSBFormat._get_buffer(framebuf)
        width = MVLSBFormat._get_width(framebuf)
        height = MVLSBFormat._get_height(framebuf)
        stride = MVLSBFormat._get_stride(framebuf, width)
        rows8 = (height + 7) // 8
        size = stride * rows8
        val = 0xFF if color else 0x00
        # Ensure we don't write beyond buffer length if provided buffer is smaller
        limit = min(size, len(buf))
        if isinstance(buf, memoryview):
            buf[:limit] = bytes([val]) * limit
        else:
            for i in range(limit):
                buf[i] = val

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        fb_width = MVLSBFormat._get_width(framebuf)
        fb_height = MVLSBFormat._get_height(framebuf)
        # Clip rectangle
        if width <= 0 or height <= 0:
            return
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(fb_width, x + width)
        y1 = min(fb_height, y + height)
        if x0 >= x1 or y0 >= y1:
            return
        # Draw by setting pixels
        for yy in range(y0, y1):
            for xx in range(x0, x1):
                MVLSBFormat.set_pixel(framebuf, xx, yy, color)
