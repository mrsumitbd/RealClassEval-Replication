class MHMSBFormat:

    @staticmethod
    def _stride(framebuf):
        return getattr(framebuf, "stride", (framebuf.width + 7) // 8)

    @staticmethod
    def _index_and_mask(framebuf, x, y):
        if x < 0 or y < 0 or x >= framebuf.width or y >= framebuf.height:
            return None, None
        stride = MHMSBFormat._stride(framebuf)
        byte_index = y * stride + (x // 8)
        bit = 7 - (x % 8)
        mask = 1 << bit
        return byte_index, mask

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        idx, mask = MHMSBFormat._index_and_mask(framebuf, x, y)
        if idx is None:
            return
        buf = framebuf.buffer
        if color:
            buf[idx] = buf[idx] | mask
        else:
            buf[idx] = buf[idx] & (~mask & 0xFF)

    @staticmethod
    def get_pixel(framebuf, x, y):
        idx, mask = MHMSBFormat._index_and_mask(framebuf, x, y)
        if idx is None:
            return 0
        return 1 if (framebuf.buffer[idx] & mask) != 0 else 0

    @staticmethod
    def fill(framebuf, color):
        val = 0xFF if color else 0x00
        buf = framebuf.buffer
        for i in range(len(buf)):
            buf[i] = val

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        if width <= 0 or height <= 0:
            return

        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(framebuf.width, x + width)
        y1 = min(framebuf.height, y + height)

        if x0 >= x1 or y0 >= y1:
            return

        buf = framebuf.buffer
        stride = MHMSBFormat._stride(framebuf)
        c1 = bool(color)

        for yy in range(y0, y1):
            row_base = yy * stride
            first_byte = x0 // 8
            last_byte = (x1 - 1) // 8

            if first_byte == last_byte:
                start_bit_in_byte = x0 % 8
                end_bit_in_byte = (x1 - 1) % 8
                head_mask = 0xFF >> start_bit_in_byte
                tail_mask = 0xFF ^ (0xFF >> (end_bit_in_byte + 1))
                mask = head_mask & tail_mask
                idx = row_base + first_byte
                if c1:
                    buf[idx] = buf[idx] | mask
                else:
                    buf[idx] = buf[idx] & (~mask & 0xFF)
            else:
                # Head byte
                head_mask = 0xFF >> (x0 % 8)
                idx = row_base + first_byte
                if c1:
                    buf[idx] = buf[idx] | head_mask
                else:
                    buf[idx] = buf[idx] & (~head_mask & 0xFF)

                # Middle full bytes
                fill_byte = 0xFF if c1 else 0x00
                for b in range(first_byte + 1, last_byte):
                    buf[row_base + b] = fill_byte

                # Tail byte
                end_bit_in_byte = (x1 - 1) % 8
                tail_mask = 0xFF ^ (0xFF >> (end_bit_in_byte + 1))
                idx = row_base + last_byte
                if c1:
                    buf[idx] = buf[idx] | tail_mask
                else:
                    buf[idx] = buf[idx] & (~tail_mask & 0xFF)
