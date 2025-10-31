class MVLSBFormat:
    '''MVLSBFormat'''
    @staticmethod
    def _bool_color(color):
        return 1 if color else 0

    @staticmethod
    def _get_stride(framebuf):
        return getattr(framebuf, "stride", framebuf.width)

    @staticmethod
    def _index_and_bit(framebuf, x, y):
        # MONO_VLSB: byte = x + (y >> 3) * stride, bit = 1 << (y & 7)
        stride = MVLSBFormat._get_stride(framebuf)
        byte_index = x + ((y >> 3) * stride)
        bit = 1 << (y & 7)
        return byte_index, bit

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        '''Set a given pixel to a color.'''
        if not (0 <= x < framebuf.width and 0 <= y < framebuf.height):
            return
        idx, bit = MVLSBFormat._index_and_bit(framebuf, x, y)
        if MVLSBFormat._bool_color(color):
            framebuf.buffer[idx] |= bit
        else:
            framebuf.buffer[idx] &= (~bit) & 0xFF

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color of a given pixel'''
        if not (0 <= x < framebuf.width and 0 <= y < framebuf.height):
            return 0
        idx, bit = MVLSBFormat._index_and_bit(framebuf, x, y)
        return 1 if (framebuf.buffer[idx] & bit) else 0

    @staticmethod
    def fill(framebuf, color):
        '''completely fill/clear the buffer with a color'''
        fill_byte = 0xFF if MVLSBFormat._bool_color(color) else 0x00
        buf = framebuf.buffer
        # Support both bytearray/memoryview
        for i in range(len(buf)):
            buf[i] = fill_byte

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        '''Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior.'''
        if width <= 0 or height <= 0:
            return

        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(framebuf.width, x + width)
        y1 = min(framebuf.height, y + height)
        if x0 >= x1 or y0 >= y1:
            return

        c = MVLSBFormat._bool_color(color)
        stride = MVLSBFormat._get_stride(framebuf)
        buf = framebuf.buffer

        # Optimize by writing whole bytes when possible
        # Process per x column as bytes represent vertical columns
        for cx in range(x0, x1):
            y_start = y0
            y_end = y1

            # Handle head partial byte
            first_block = y_start >> 3
            last_block = (y_end - 1) >> 3

            if first_block == last_block:
                # Region within a single byte
                idx = cx + first_block * stride
                mask = 0
                for py in range(y_start, y_end):
                    mask |= (1 << (py & 7))
                if c:
                    buf[idx] |= mask
                else:
                    buf[idx] &= (~mask) & 0xFF
                continue

            # Head partial
            if (y_start & 7) != 0:
                idx = cx + first_block * stride
                mask = 0
                for py in range(y_start, (first_block + 1) * 8):
                    mask |= (1 << (py & 7))
                if c:
                    buf[idx] |= mask
                else:
                    buf[idx] &= (~mask) & 0xFF
                first_block += 1

            # Full bytes
            if first_block <= last_block - 1:
                fill_byte = 0xFF if c else 0x00
                for blk in range(first_block, last_block):
                    idx = cx + blk * stride
                    buf[idx] = fill_byte

            # Tail partial
            idx = cx + last_block * stride
            mask = 0
            for py in range(last_block * 8, y_end):
                mask |= (1 << (py & 7))
            if c:
                buf[idx] |= mask
            else:
                buf[idx] &= (~mask) & 0xFF
