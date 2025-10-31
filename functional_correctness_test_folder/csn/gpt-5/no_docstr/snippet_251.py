class MVLSBFormat:

    @staticmethod
    def _get_buf(framebuf):
        buf = getattr(framebuf, "buffer", None)
        if buf is None:
            buf = getattr(framebuf, "buf", None)
        if buf is None:
            raise AttributeError("framebuf must have 'buffer' or 'buf'")
        return buf

    @staticmethod
    def _rows_in_bytes(height):
        return (height + 7) // 8

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        w = getattr(framebuf, "width")
        h = getattr(framebuf, "height")
        if x < 0 or y < 0 or x >= w or y >= h:
            return
        buf = MVLSBFormat._get_buf(framebuf)
        rows = MVLSBFormat._rows_in_bytes(h)
        idx = x * rows + (y >> 3)
        bit = 1 << (y & 7)
        if color:
            buf[idx] = buf[idx] | bit
        else:
            buf[idx] = buf[idx] & (~bit & 0xFF)

    @staticmethod
    def get_pixel(framebuf, x, y):
        w = getattr(framebuf, "width")
        h = getattr(framebuf, "height")
        if x < 0 or y < 0 or x >= w or y >= h:
            return 0
        buf = MVLSBFormat._get_buf(framebuf)
        rows = MVLSBFormat._rows_in_bytes(h)
        idx = x * rows + (y >> 3)
        bit = 1 << (y & 7)
        return 1 if (buf[idx] & bit) else 0

    @staticmethod
    def fill(framebuf, color):
        w = getattr(framebuf, "width")
        h = getattr(framebuf, "height")
        buf = MVLSBFormat._get_buf(framebuf)
        val = 0xFF if color else 0x00
        # Fill all bytes
        for i in range(len(buf)):
            buf[i] = val
        # Optional: mask unused bits in last byte of each column when setting to 1
        # to ensure out-of-bounds bits are cleared. This keeps behavior clean.
        if color:
            rem = h & 7
            if rem != 0:
                rows = MVLSBFormat._rows_in_bytes(h)
                mask = (1 << rem) - 1  # bits [0..rem-1] set
                for x in range(w):
                    idx = x * rows + (rows - 1)
                    buf[idx] &= mask

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        fb_w = getattr(framebuf, "width")
        fb_h = getattr(framebuf, "height")
        if width <= 0 or height <= 0:
            return

        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(fb_w, x + width)
        y1 = min(fb_h, y + height)
        if x0 >= x1 or y0 >= y1:
            return

        buf = MVLSBFormat._get_buf(framebuf)
        rows = MVLSBFormat._rows_in_bytes(fb_h)

        y0_byte = y0 >> 3
        y1_byte = (y1 - 1) >> 3
        y0_bit = y0 & 7
        y1_bit = (y1 - 1) & 7

        for xi in range(x0, x1):
            base = xi * rows
            if y0_byte == y1_byte:
                # Rectangle within the same byte
                mask = ((0xFF << y0_bit) & (0xFF >> (7 - y1_bit))) & 0xFF
                idx = base + y0_byte
                if color:
                    buf[idx] = buf[idx] | mask
                else:
                    buf[idx] = buf[idx] & (~mask & 0xFF)
            else:
                # First partial byte
                first_mask = (0xFF << y0_bit) & 0xFF
                idx = base + y0_byte
                if color:
                    buf[idx] = buf[idx] | first_mask
                else:
                    buf[idx] = buf[idx] & (~first_mask & 0xFF)

                # Middle full bytes
                for b in range(y0_byte + 1, y1_byte):
                    idx = base + b
                    buf[idx] = 0xFF if color else 0x00

                # Last partial byte
                last_mask = 0xFF >> (7 - y1_bit)
                idx = base + y1_byte
                if color:
                    buf[idx] = buf[idx] | last_mask
                else:
                    buf[idx] = buf[idx] & (~last_mask & 0xFF)
