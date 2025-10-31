class MHMSBFormat:
    @staticmethod
    def _get_attr(obj, *names):
        for n in names:
            if isinstance(obj, dict) and n in obj:
                return obj[n]
            if hasattr(obj, n):
                return getattr(obj, n)
        raise AttributeError(f"Missing attributes {names}")

    @staticmethod
    def _get_buf(framebuf):
        return MHMSBFormat._get_attr(framebuf, 'buf', 'buffer', 'data')

    @staticmethod
    def _get_width(framebuf):
        return int(MHMSBFormat._get_attr(framebuf, 'width', 'w'))

    @staticmethod
    def _get_height(framebuf):
        return int(MHMSBFormat._get_attr(framebuf, 'height', 'h'))

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        '''Set a given pixel to a color.'''
        buf = MHMSBFormat._get_buf(framebuf)
        width = MHMSBFormat._get_width(framebuf)
        height = MHMSBFormat._get_height(framebuf)

        if not (0 <= x < width and 0 <= y < height):
            return

        stride = (width + 7) // 8
        idx = y * stride + (x >> 3)
        bit = 7 - (x & 7)
        mask = 1 << bit
        if color:
            buf[idx] = buf[idx] | mask
        else:
            buf[idx] = buf[idx] & (~mask & 0xFF)

    @staticmethod
    def get_pixel(framebuf, x, y):
        buf = MHMSBFormat._get_buf(framebuf)
        width = MHMSBFormat._get_width(framebuf)
        height = MHMSBFormat._get_height(framebuf)

        if not (0 <= x < width and 0 <= y < height):
            return 0

        stride = (width + 7) // 8
        idx = y * stride + (x >> 3)
        bit = 7 - (x & 7)
        return (buf[idx] >> bit) & 1

    @staticmethod
    def fill(framebuf, color):
        '''completely fill/clear the buffer with a color'''
        buf = MHMSBFormat._get_buf(framebuf)
        width = MHMSBFormat._get_width(framebuf)
        height = MHMSBFormat._get_height(framebuf)

        stride = (width + 7) // 8
        used = stride * height
        val = 0xFF if color else 0x00
        # Only fill the portion that maps to the frame dimensions
        mv = memoryview(buf)
        mv[:used] = bytes([val]) * used

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        '''Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior.'''
        buf = MHMSBFormat._get_buf(framebuf)
        fb_w = MHMSBFormat._get_width(framebuf)
        fb_h = MHMSBFormat._get_height(framebuf)
        stride = (fb_w + 7) // 8

        if width <= 0 or height <= 0:
            return

        # Clip rectangle
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(fb_w, x + width)
        y1 = min(fb_h, y + height)

        if x0 >= x1 or y0 >= y1:
            return

        set_val = bool(color)

        for yy in range(y0, y1):
            row_base = yy * stride

            xs = x0
            xe = x1

            # First partial byte
            first_byte_index = xs >> 3
            last_byte_index = (xe - 1) >> 3

            if first_byte_index == last_byte_index:
                # All within one byte
                start_bit = 7 - (xs & 7)
                end_bit = 7 - ((xe - 1) & 7)
                # Bits from end_bit to start_bit inclusive
                mask = ((0xFF >> end_bit) & (0xFF << (7 - start_bit))) & 0xFF
                idx = row_base + first_byte_index
                if set_val:
                    buf[idx] = buf[idx] | mask
                else:
                    buf[idx] = buf[idx] & (~mask & 0xFF)
            else:
                # First partial
                start_bit = 7 - (xs & 7)
                first_mask = (0xFF << (7 - start_bit)) & 0xFF
                idx = row_base + first_byte_index
                if start_bit == 7:
                    first_mask = 0xFF  # xs aligned to byte start
                if xs & 7 == 0:
                    first_mask = 0xFF
                if set_val:
                    buf[idx] = buf[idx] | first_mask
                else:
                    buf[idx] = buf[idx] & (~first_mask & 0xFF)

                # Middle full bytes
                for b in range(first_byte_index + 1, last_byte_index):
                    idx = row_base + b
                    buf[idx] = 0xFF if set_val else 0x00

                # Last partial
                end_bit = 7 - ((xe - 1) & 7)
                last_mask = 0xFF >> end_bit
                idx = row_base + last_byte_index
                if ((xe - 1) & 7) == 7:
                    last_mask = 0xFF
                if set_val:
                    buf[idx] = buf[idx] | last_mask
                else:
                    buf[idx] = buf[idx] & (~last_mask & 0xFF)
